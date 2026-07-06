import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Note
from .serializers import NoteSerializer, UserSerializer

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text_with_groq(text):
    prompt = (
        "Summarize the following note in 2-3 short bullet points or a brief paragraph. "
        "Keep it concise and useful.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=150,
    )

    return response.choices[0].message.content


def summarize_text_locally(text):
    return "API is not working right now. Please try again later."


# Create your views here.
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class=NoteSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset (self):
        user=self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self,serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user) 
        else:
            print(serializer.errors)
class NoteDelete(generics.DestroyAPIView):
    serializer_class=NoteSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset (self):
        user=self.request.user
        return Note.objects.filter(author=user)


class NoteSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        note = get_object_or_404(Note.objects.filter(author=request.user), pk=pk)
        try:
           

            summary = summarize_text_with_groq(note.content)
            return Response({"summary": summary})
        
        except Exception as exc:
            fallback_summary = summarize_text_locally(note.content)
            return Response(
                {"summary": fallback_summary, "fallback": True},
                status=status.HTTP_200_OK,
            )


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print("DATA:", request.data)  # 👈 check request payload
        return super().create(request, *args, **kwargs)