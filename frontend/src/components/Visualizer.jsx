import React, { useEffect, useRef } from "react";
import "../styles/Visualizer.css"; // Import the stylesheet

const Visualizer = ({ predictions, benchmarks }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;

    // Set canvas size for high DPI displays
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    // Clear canvas
    ctx.clearRect(0, 0, rect.width, rect.height);

    // Define sizes and margins
    const padding = 50;
    const width = rect.width - 2 * padding;
    const height = rect.height - 2 * padding;

    // Scaling functions
    const maxX = 800;
    const maxY = 600;
    const scaleX = (x) => padding + (x / maxX) * width;
    const scaleY = (y) => rect.height - padding - (y / maxY) * height;

    // Draw gridlines
    ctx.strokeStyle = "#ddd";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 10; i++) {
      const x = padding + (i / 10) * width;
      const y = rect.height - padding - (i / 10) * height;

      // Vertical gridline
      ctx.beginPath();
      ctx.moveTo(x, padding);
      ctx.lineTo(x, rect.height - padding);
      ctx.stroke();

      // Horizontal gridline
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(rect.width - padding, y);
      ctx.stroke();
    }

    // Draw axes
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, rect.height - padding);
    ctx.lineTo(rect.width - padding, rect.height - padding);
    ctx.stroke();

    // Add labels
    ctx.font = "14px Arial";
    ctx.fillStyle = "#000";
    ctx.fillText("X Axis", rect.width / 2, rect.height - 10);
    ctx.save();
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Y Axis", -rect.height / 2, 20);
    ctx.restore();

    // Add smooth data points
    const drawPoint = (x, y, color, size = 6) => {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, size, 0, 2 * Math.PI);
      ctx.shadowColor = "rgba(0,0,0,0.3)";
      ctx.shadowBlur = 4;
      ctx.fill();
    };

    // Draw predictions (blue)
    predictions.forEach(([x, y]) => {
      drawPoint(scaleX(x), scaleY(y), "#007bff");
    });

    // Draw benchmarks (red)
    benchmarks.forEach(([x, y]) => {
      drawPoint(scaleX(x), scaleY(y), "#dc3545");
    });

    // Add legend
    ctx.shadowBlur = 0;
    ctx.fillStyle = "#007bff";
    ctx.fillRect(padding + 10, 10, 12, 12);
    ctx.fillStyle = "#000";
    ctx.fillText("Predictions", padding + 30, 20);

    ctx.fillStyle = "#dc3545";
    ctx.fillRect(padding + 10, 30, 12, 12);
    ctx.fillStyle = "#000";
    ctx.fillText("Benchmarks", padding + 30, 40);
  }, [predictions, benchmarks]);

  return (
    <div className="visualizer-container">
      <div className="visualizer-wrapper">
        <h3 className="visualizer-title">Predictions vs Benchmarks</h3>
        <canvas ref={canvasRef} className="visualizer-canvas" />
      </div>
    </div>
  );
};

export default Visualizer;
