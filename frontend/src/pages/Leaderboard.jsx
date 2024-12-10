import React, { useState, useEffect } from "react";
import api from "../api";
import "../styles/Submit.css";

const METRICS = {
  "LR": ["accuracy"],
  "Saccade": [],
  "Fixation": ["euclidean_distance_sum", "l1_distance_sum"],
  "Segmentation": [],
  "Scanpath": []
}

const Leaderboard = () => {
  const tabs = ["LR", "Saccade", "Fixation", "Segmentation", "Scanpath", "Path"];

  const [activeTab, setActiveTab] = useState("LR"); // Default tab is "LR"
  const [submissions, setSubmissions] = useState([]);
  const [selectedAggregation, setSelectedAggregation] = useState("Overall");
  const [selectedMetric, setSelectedMetric] = useState("accuracy");

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = () => {
    api
      .get("/api/submissions/all/")
      .then((res) => res.data)
      .then((data) => {
        console.log("Fetched submissions:", data);
        setSubmissions(data);
      })
      .catch((err) => alert("tress"));
  };

  // Filter submissions based on the active tab
  const filteredSubmissions = submissions.filter(
    (submission) => submission.task === activeTab
  );

  return (
    <div className="submit-page">
      <div className="tabs-container">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`tab-button ${activeTab === tab ? "active" : ""}`}
            onClick={() => {
                setActiveTab(tab);
                setSelectedAggregation(METRICS[tab])
              }
            }
          >
            {tab + " Task"}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {/* <h1>{activeTab + " Task"}</h1> */}

        <div className="file-list">
          <h1>Leaderboard</h1>
          {filteredSubmissions.length > 0 ? (
            <>
              <div className="dropdown-container">
                <select
                  className="dropdown"
                  value={selectedAggregation}
                  onChange={(e) => setSelectedAggregation(e.target.value)}
                  disabled={filteredSubmissions.length === 0} // Disable if no submissions
                >
                  {filteredSubmissions[0]?.score?.index?.map((key) => (
                    <option key={key} value={key}>
                      {key}
                    </option>
                  ))}
                </select>

                <select
                  className="dropdown"
                  value={selectedMetric}
                  onChange={(e) => setSelectedMetric(e.target.value)}
                  disabled={filteredSubmissions.length === 0} // Disable if no submissions
                >
                  {filteredSubmissions[0]?.score?.columns?.map((key) => (
                    <option key={key} value={key}>
                      {key}
                    </option>
                  ))}
                </select>
              </div>
              <table>
                <thead>
                  <tr>
                    <th>User</th>
                    <th>Aggregation</th>
                    <th>Metric</th>
                    <th>Score</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSubmissions.map((submission) => (
                    <tr key={submission.id}>
                      <td>{submission.username}</td>
                      <td>{selectedAggregation}</td>
                      <td>{selectedMetric}</td>
                      <td>
                        {(() => {
                          const rowIndex = submission.score?.index.indexOf(selectedAggregation); // Find row index
                          const colIndex = submission.score?.columns.indexOf(selectedMetric);   // Find column index
                          
                          if (rowIndex !== -1 && colIndex !== -1) {
                            return submission.score?.data[rowIndex][colIndex]; // Access data using indices
                          }
                          return "error"; // Default value if row/column not found
                        })()}
                      </td>
                      <td>
                        <button
                          onClick={() => deleteSubmission(submission.id)}
                          className="delete-button"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
            
          ) : (
            <p>No submissions available for {activeTab}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
