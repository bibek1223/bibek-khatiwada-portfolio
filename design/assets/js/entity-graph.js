/**
 * Lightweight 3D Entity Knowledge Graph Canvas (< 3KB)
 * Zero external libraries. 60 FPS requestAnimationFrame with IntersectionObserver pause.
 */
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.dashboard-photo-card');
  if (!container) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  const canvas = document.createElement('canvas');
  canvas.className = 'entity-graph-canvas';
  container.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  let width, height;
  let isVisible = true;
  let mouseX = 0, mouseY = 0;
  let targetRotX = 0, targetRotY = 0;
  let rotX = 0, rotY = 0;

  function resize() {
    width = canvas.width = container.offsetWidth;
    height = canvas.height = container.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // 12 Semantically Named Nodes (Icosahedron / Entity Lattice)
  const labels = [
    "Entity", "Attribute", "Value", "AEO", "llms.txt", "Crawl",
    "Vector", "Schema", "RAG", "Embed", "Graph", "GSC"
  ];

  const nodes = [];
  const phi = (1 + Math.sqrt(5)) / 2;
  const rawVertices = [
    [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
    [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
    [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1]
  ];

  const scale = 75;
  rawVertices.forEach((v, i) => {
    nodes.push({
      x: v[0] * scale,
      y: v[1] * scale,
      z: v[2] * scale,
      label: labels[i] || ""
    });
  });

  // Calculate edges between closest nodes (unit distance in icosahedron is 2)
  const edges = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dz = nodes[i].z - nodes[j].z;
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      if (dist < scale * 2.1) {
        edges.push([i, j]);
      }
    }
  }

  container.addEventListener('mousemove', (e) => {
    const rect = container.getBoundingClientRect();
    mouseX = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
    mouseY = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
    targetRotY = mouseX * 0.8;
    targetRotX = -mouseY * 0.8;
  });

  container.addEventListener('mouseleave', () => {
    targetRotX = 0;
    targetRotY = 0;
  });

  // Pause offscreen
  const observer = new IntersectionObserver(([entry]) => {
    isVisible = entry.isIntersecting;
  }, { threshold: 0.1 });
  observer.observe(container);

  let angle = 0;
  function render() {
    if (!isVisible) {
      requestAnimationFrame(render);
      return;
    }

    ctx.clearRect(0, 0, width, height);

    angle += 0.006;
    rotX += (targetRotX - rotX) * 0.05;
    rotY += (targetRotY - rotY) * 0.05;

    const currentRotY = angle + rotY;
    const currentRotX = Math.sin(angle * 0.5) * 0.2 + rotX;

    const cosY = Math.cos(currentRotY), sinY = Math.sin(currentRotY);
    const cosX = Math.cos(currentRotX), sinX = Math.sin(currentRotX);

    const cx = width / 2;
    const cy = height / 2;
    const fov = 350;

    const projected = nodes.map(n => {
      // Y rotation
      let x1 = n.x * cosY + n.z * sinY;
      let z1 = -n.x * sinY + n.z * cosY;
      // X rotation
      let y2 = n.y * cosX - z1 * sinX;
      let z2 = n.y * sinX + z1 * cosX;

      const pScale = fov / (fov + z2 + 100);
      return {
        px: cx + x1 * pScale,
        py: cy + y2 * pScale,
        pz: z2,
        scale: pScale,
        label: n.label
      };
    });

    // Draw Edges
    ctx.lineWidth = 1.2;
    edges.forEach(([i, j]) => {
      const p1 = projected[i];
      const p2 = projected[j];
      const alpha = Math.max(0.1, Math.min(0.6, (p1.scale + p2.scale) * 0.3));
      ctx.strokeStyle = `rgba(124, 58, 237, ${alpha})`;
      ctx.beginPath();
      ctx.moveTo(p1.px, p1.py);
      ctx.lineTo(p2.px, p2.py);
      ctx.stroke();
    });

    // Draw Nodes
    projected.forEach(p => {
      const radius = Math.max(2, 4.5 * p.scale);
      ctx.fillStyle = '#7c3aed';
      ctx.beginPath();
      ctx.arc(p.px, p.py, radius, 0, Math.PI * 2);
      ctx.fill();

      // Small node labels for technical flair
      if (p.scale > 0.85) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
        ctx.font = '9px monospace';
        ctx.fillText(p.label, p.px + 6, p.py + 3);
      }
    });

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
});
