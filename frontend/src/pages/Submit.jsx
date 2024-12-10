import React, { useState, useEffect } from "react";
import api from "../api";
import "../styles/Submit.css";
import Visualizer from "../components/Visualizer";

const METRICS = {
  "LR": ["accuracy"],
  "Saccade": [],
  "Fixation": ["euclidean_distance_sum", "l1_distance_sum"],
  "Segmentation": [],
  "Scanpath": []
}

const Submit = () => {
  const tabs = ["LR", "Saccade", "Fixation", "Segmentation", "Scanpath", "Path"];

  const [activeTab, setActiveTab] = useState("LR"); 
  const [submissions, setSubmissions] = useState([]);
  const [file, setFile] = useState(null);
  const [selectedAggregation, setSelectedAggregation] = useState("Overall");
  const [selectedMetric, setSelectedMetric] = useState("accuracy");
  const [showVisualizer, setShowVisualizer] = useState(false); 
  const [visulizationData, setVisualizationData] = useState(
    {predictions: [], benchmarks: []}
  );
  const [isLoading, setIsLoading] = useState(false);


  useEffect(() => {
    fetchSubmissions();
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files ? event.target.files[0] : null);
  };

  const fetchSubmissions = () => {
    api
      .get("/api/submissions/")
      .then((res) => res.data)
      .then((data) => {
        console.log("Fetched submissions:", data);
        setSubmissions(data);
      })
      .catch((err) => alert(err));
  };

  const createSubmission = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("task", activeTab); // Add the string (task)

    api
      .post("/api/submissions/create/", formData)
      .then((res) => {
        if (res.status === 201) console.log("Submission created!");
        else alert("Failed to make a submission");
        fetchSubmissions();
      })
      .catch((err) => alert(err));
  };

  const deleteSubmission = (id) => {
    api
        .delete(`/api/submission/delete/${id}/`)
        .then((res) => {
            fetchSubmissions();
        })
        .catch((error) => alert(error));
  };

  const visualizeSubmission = (e) => {
    setIsLoading(true);
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("task", activeTab); // Add the string (task)

    api
      .post("/api/visualize/", formData)
      .then((res) => JSON.parse(res.data))
      .then((data) => {
        console.log("Fetched visualizationData:", typeof data);
        setVisualizationData({
          predictions: data.predictions || [],
          benchmarks: data.benchmarks || [],
        });
        setShowVisualizer(true);
      })
      .catch((err) => alert(err))
      .finally(() => setIsLoading(false))
      
  }

  const closeVisualization = () => {
    setShowVisualizer(false)
  }

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
                setSelectedMetric(METRICS[tab])
              }
            }
          >
            {tab + " Task"}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {/* <h1>{activeTab + " Task"}</h1> */}
        <form onSubmit={createSubmission}>
          <input type="file" onChange={handleFileChange} />

          {/* Benchmark Button */}
          <button type="submit" disabled={!file}>
            Benchmark
          </button>

          {/* Visualize Button */}
          <button
            type="button" // Prevents form submission
            className="visualize-button"
            disabled={!file}
            onClick={visualizeSubmission} // Separate event handler
          >
            Visualize
          </button>
        </form>

        {/* Loading indicator */}
        {isLoading && <p>Loading...</p>}

        {/* Conditionally render the Visualizer */}
        {showVisualizer && (
          <div className="visualizer-container">
            <Visualizer
              predictions={visulizationData.predictions}
              benchmarks={visulizationData.benchmarks}
            />
            {/* Button to close visualization */}
            <button
              className="close-button"
              onClick={closeVisualization}
            >
              Close Visualization
            </button>
          </div>
        )}

        <div className="file-list">
          <h1>Submissions</h1>
          {filteredSubmissions.length > 0 ? (
            <>
              <div className="dropdown-container">
                <h4>Select Aggregation</h4>
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
                <h4>Select Metric</h4>
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
                    <th>File Name</th>
                    <th>
                      Aggregation
                    </th>
                    <th>Metric</th>
                    <th>Score</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSubmissions.map((submission) => (
                    <tr key={submission.id}>
                      <td>{submission.fileName}</td>
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

export default Submit;
