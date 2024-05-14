import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import SetRates from "./pages/SetRates";
import GetRates from "./pages/GetRates";
import FileUpload from "./pages/FileUpload";

const BASE_API = "http://127.0.0.1:8000/psql/";

function App() {
  const [keys, setKeys] = useState([]);
  const [rates, setRates] = useState();
  useEffect(() => {
    const getRate = async () => {
      try {
        const response = await fetch(BASE_API + "get-rate/");
        if (!response.ok) throw new Error("Response not ok");

        const data = await response.json();
        const fields = data.map((i) => i.fields);
        setRates(fields);
        setKeys(Object.keys(fields[0]));
      } catch (error) {
        console.error(error);
      }
    };
    getRate();
  }, []);

  return (
    <BrowserRouter>
      <div className="app">
        <nav>
          <ul>
            <li>
              <Link to="/">Rates</Link>
            </li>
            <li>
              <Link to="/set-rate">Set Rates</Link>
            </li>
            <li>
              <Link to="/file-upload">File Upload</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route
            path="/"
            element={<GetRates rates={rates} keys={keys} BASE_API={BASE_API} />}
          />
          <Route
            path="set-rate"
            element={<SetRates rates={rates} keys={keys} BASE_API={BASE_API} />}
          />
          <Route
            path="file-upload"
            element={<FileUpload BASE_API={BASE_API} />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
