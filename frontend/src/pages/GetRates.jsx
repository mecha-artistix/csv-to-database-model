function GetRates({ keys, rates }) {
  return (
    <div className="right">
      <h1>Get Rates</h1>
      {keys.length > 0 && rates.length > 0 && (
        <table>
          <thead>
            <tr>
              {keys.map((item, i) => (
                <th key={i}>{item}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rates.map((rate, i) => (
              <tr key={i}>
                {keys.map((col, i) => (
                  <td key={i}>{rate[col]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default GetRates;
