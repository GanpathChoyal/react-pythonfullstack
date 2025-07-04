import React from "react";
import api from "../api";
import { useEffect,useState } from "react";
import Note from "../components/Note";
import "../styles/Home.css"


export default function Home() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  useEffect(() => {
    getNotes();
  }, []);

  const getNotes = () => {
    api
      .get("/api/notes")
      .then((res) => res.data)
      .then((data) => {
        setNotes(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };
  const deleteNote = (id) => {
    api
      .delete(`/api/notes/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) alert("Note deleted");
        else alert("failed to delete note");
         getNotes();
      })
      .catch((error) => alert(error));
   
  };
  const createNote = (e) => {
    e.preventDefault();
    api
      .post("/api/notes/", { content, title })
      .then((rest) => {
        if (rest.status === 201) alert("Note created");
        else alert("Failed to create note");
        getNotes();
      })
      .catch((error) => alert(error));
    
  };
  return (
    <div>
      <div>
        <h2>Notes</h2>
        {notes.map((note)=>(<Note note={note} onDelete={deleteNote} key={note.id}/>)) }
      </div>
      <form onSubmit={createNote}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
          type="text"
          id="title"
          name="title"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
          <br />
        <label htmlFor="content">Content</label>
        <br />
        <textarea
          id="content"
          name="content"
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        >
         
        </textarea>
        <br />
        <input type="submit" value="submit"></input>
      </form>
    </div>
  );
}
