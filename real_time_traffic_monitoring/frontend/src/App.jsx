import React, { useEffect, useRef, useState } from "react";

const WS_URL = "ws://127.0.0.1:8000/ws/traffic";

function Card({ title, value }) {
  return (
    <div className="card">
      <span>{title}</span>
      <b>{value}</b>
    </div>
  );
}

export default function App() {
  const video = useRef(null);
  const canvas = useRef(null);
  const output = useRef(null);
  const socket = useRef(null);
  const timer = useRef(null);

  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    total: 0,
    counts: {car:0, motorcycle:0, bus:0, truck:0},
    violations: 0,
    density: "Low"
  });

  useEffect(() => () => stop(), []);

  async function start() {
    try {
      setError("");

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false
      });

      video.current.srcObject = stream;
      await video.current.play();

      const ws = new WebSocket(WS_URL);
      socket.current = ws;

      ws.onopen = () => {
        setRunning(true);
        sendFrame();
      };

      ws.onmessage = e => {
        const data = JSON.parse(e.data);
        if (data.stats) setStats(data.stats);
        if (data.image && output.current) {
          output.current.src = "data:image/jpeg;base64," + data.image;
        }
      };

      ws.onerror = () => setError("Backend connection failed.");
    } catch {
      setError("Camera permission failed or backend is not running.");
    }
  }

  function sendFrame() {
    if (!running && socket.current?.readyState !== WebSocket.OPEN) return;

    const v = video.current;
    const c = canvas.current;
    const ws = socket.current;

    if (!v || !c || !ws || ws.readyState !== WebSocket.OPEN) return;

    c.width = 640;
    c.height = 480;
    c.getContext("2d").drawImage(v, 0, 0, 640, 480);

    c.toBlob(blob => {
      if (!blob || socket.current?.readyState !== WebSocket.OPEN) return;

      const reader = new FileReader();
      reader.onloadend = () => socket.current?.send(reader.result);
      reader.readAsDataURL(blob);
    }, "image/jpeg", 0.65);

    timer.current = setTimeout(sendFrame, 150);
  }

  function stop() {
    setRunning(false);
    clearTimeout(timer.current);

    const stream = video.current?.srcObject;
    stream?.getTracks().forEach(t => t.stop());

    if (video.current) video.current.srcObject = null;
    socket.current?.close();
    socket.current = null;
  }

  return (
    <div className="app">
      <header>
        <div>
          <h1>AI Traffic Monitoring</h1>
          <p>Real-time vehicle detection and lane monitoring</p>
        </div>
        <div className={running ? "status live" : "status"}>
          ● {running ? "LIVE" : "OFFLINE"}
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <section className="stats">
        <Card title="Vehicles" value={stats.total}/>
        <Card title="Cars" value={stats.counts.car}/>
        <Card title="Motorcycles" value={stats.counts.motorcycle}/>
        <Card title="Buses" value={stats.counts.bus}/>
        <Card title="Trucks" value={stats.counts.truck}/>
        <Card title="Violations" value={stats.violations}/>
        <Card title="Density" value={stats.density}/>
      </section>

      <main>
        <section className="panel">
          <h2>Live AI Camera</h2>
          <video ref={video} muted playsInline className="hidden"/>
          <canvas ref={canvas} className="hidden"/>
          <div className="screen">
            {running
              ? <img ref={output} alt="AI traffic feed"/>
              : <div className="placeholder">
                  <div>📷</div>
                  <p>Start monitoring to begin detection</p>
                </div>
            }
          </div>
          <button onClick={running ? stop : start}>
            {running ? "Stop Monitoring" : "Start Monitoring"}
          </button>
        </section>

        <aside className="panel">
          <h2>AI System</h2>
          <p><b>Model:</b> YOLO11 Nano</p>
          <p><b>Backend:</b> FastAPI</p>
          <p><b>Frontend:</b> React</p>
          <p><b>Transport:</b> WebSocket</p>
          <p><b>Database:</b> SQLite</p>

          <h2>Detection</h2>
          <ul>
            <li>Green box = vehicle</li>
            <li>Red box = restricted-lane violation</li>
            <li>Density updates in real time</li>
          </ul>
        </aside>
      </main>
    </div>
  );
}
