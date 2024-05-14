import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";

const BASE_API = "http://127.0.0.1:8000/file/";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [content, setContent] = useState("");

  // API USING AXIOS
  const sendData = () => {
    console.log(file.name, content);
    axios
      .post(BASE_API + "receive-data/", {
        fileName: file.name,
        fileContent: content,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    if (content.length > 1) sendData();
  }, [content]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile); // Update state to hold the currently selected file
    }
  };
  const handleFileSubmit = (e) => {
    e.preventDefault();
    if (file) {
      // Make sure there's a file selected
      const fr = new FileReader();
      fr.readAsText(file); // Read the file as text
      fr.onload = () => {
        setContent(fr.result); // Set content state to the contents of the file
      };
    }
  };

  const Table = ({ content }) => {
    const array = content.split(/\r\n|\n|\r/).map((line) => line.split(","));
    console.log(array);

    return (
      <>
        {array.length > 1 && (
          <table>
            {array.map((line, i) =>
              i == 0 ? (
                <thead key={i}>
                  <tr>
                    {line.map((cell) => (
                      <th>{cell}</th>
                    ))}
                  </tr>
                </thead>
              ) : (
                <tbody>
                  <tr>
                    {line.map((cell) => (
                      <td>{cell}</td>
                    ))}
                  </tr>
                </tbody>
              )
            )}
          </table>
        )}
      </>
    );
  };

  return (
    <div>
      <h1>File Upload</h1>
      <form onSubmit={handleFileSubmit}>
        <input type="file" onChange={handleFileChange} />
        <input type="submit" value="Upload File" />
      </form>
      <div>
        <p>File content:</p>
        <Table content={content} />
      </div>
    </div>
  );
}

export default FileUpload;
