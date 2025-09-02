const video = document.getElementById('cam');
const overlay = document.getElementById('overlay');
const capture = document.getElementById('capture');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const fpsEl = document.getElementById('fps');
const statusEl = document.getElementById('status');

let running = false;
let lastTime = performance.now();
let frames = 0;
let timer = null;
const intervalMs = 300;

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: 'environment' }, audio: false
  });
  video.srcObject = stream;
  await video.play();

  const w = video.videoWidth;
  const h = video.videoHeight;
  overlay.width = w; overlay.height = h;
  capture.width = w; capture.height = h;
}

function drawBoxes(ctx, boxes) {
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  ctx.lineWidth = 2;
  ctx.font = '14px system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial';
  ctx.strokeStyle = 'red';
  ctx.fillStyle = 'red';
  boxes.forEach(b => {
    const pts = b.points;
    if (!pts || pts.length === 0) return;
    ctx.beginPath();
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
    ctx.closePath();
    ctx.stroke();
    const [x, y] = pts[0];
    if (typeof b.score === 'number') ctx.fillText(b.score.toFixed(2), x, y - 4);
  });
}

async function captureAndSend() {
  if (!running) return;

  const ctx = capture.getContext('2d');
  ctx.drawImage(video, 0, 0, capture.width, capture.height);
  const dataUrl = capture.toDataURL('image/jpeg', 0.8);

  statusEl.textContent = 'Detecting…';
  try {
    const res = await fetch('/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: dataUrl, width: capture.width, height: capture.height })
    });
    const json = await res.json();
    const ctxOverlay = overlay.getContext('2d');
    drawBoxes(ctxOverlay, json.boxes || []);
    statusEl.textContent = `Boxes: ${(json.boxes || []).length}`;
  } catch (e) {
    statusEl.textContent = 'Error';
    console.error(e);
  }

  frames++;
  const now = performance.now();
  if (now - lastTime >= 1000) {
    fpsEl.textContent = `FPS: ${frames}`;
    frames = 0; lastTime = now;
  }
}

startBtn.onclick = async () => {
  if (running) return;
  await startCamera();
  running = true;
  startBtn.disabled = true; stopBtn.disabled = false;
  timer = setInterval(captureAndSend, intervalMs);
};

stopBtn.onclick = () => {
  running = false;
  startBtn.disabled = false; stopBtn.disabled = true;
  if (timer) clearInterval(timer);
  const stream = video.srcObject; if (stream) stream.getTracks().forEach(t => t.stop());
  statusEl.textContent = 'Stopped';
};
