import React from "react";
import { useState } from "react";
function SetRates({ BASE_API, rates, keys }) {
  const [formData, setFormData] = useState({});
  const createRate = async () => {
    try {
      const response = await fetch(BASE_API + "create-rate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) throw new Error("jo marzi");

      if (response.status === 200) console.log("entries already exist");
      if (response.status === 201) console.log("entries posted");
    } catch (error) {
      console.log("Failed to log in:", error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("submit :", formData);
    createRate();
  };
  return (
    <div className="left">
      <h1>Create Rates</h1>
      <form onSubmit={handleSubmit}>
        {keys.map((item, i) => (
          <div className="form-field" key={i}>
            <label>{item}</label>
            <input
              type={typeof rates[0][item]}
              name={item}
              value={formData[item] || ""}
              onChange={handleChange}
            />
            <p>{typeof rates[0][item]}</p>
          </div>
        ))}
        <input type="submit" />
      </form>
    </div>
  );
}

export default SetRates;
