// CleanSociety — main.js

document.addEventListener('DOMContentLoaded', () => {

  // ── FLASH AUTO-DISMISS ────────────────────────
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s, transform 0.5s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-8px)';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });

  // ── LIGHTBOX ──────────────────────────────────
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  if (lightbox) {
    document.querySelectorAll('.report-thumb').forEach(img => {
      img.addEventListener('click', () => {
        lightboxImg.src = img.src;
        lightbox.classList.add('open');
      });
    });
    lightbox.addEventListener('click', e => {
      if (e.target === lightbox || e.target.classList.contains('lightbox-close')) {
        lightbox.classList.remove('open');
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') lightbox.classList.remove('open');
    });
  }

  // ── PROFILE PHOTO PREVIEW ─────────────────────
  const profilePhotoInput = document.getElementById('profile_photo_input');
  const profilePhotoPreview = document.getElementById('profile_photo_preview');
  if (profilePhotoInput && profilePhotoPreview) {
    profilePhotoInput.addEventListener('change', () => {
      const file = profilePhotoInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          profilePhotoPreview.src = e.target.result;
          profilePhotoPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── REPORT FILE UPLOAD PREVIEW ────────────────
  const photoInput = document.getElementById('photo_input');
  const photoPreview = document.getElementById('photo_file_preview');
  if (photoInput && photoPreview) {
    photoInput.addEventListener('change', () => {
      const file = photoInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          photoPreview.src = e.target.result;
          photoPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ── CAMERA ────────────────────────────────────
  const openCamBtn    = document.getElementById('open-camera');
  const closeCamBtn   = document.getElementById('close-camera');
  const captureBtn    = document.getElementById('capture-btn');
  const retakeBtn     = document.getElementById('retake-btn');
  const camStream     = document.getElementById('camera-stream');
  const capturedPrev  = document.getElementById('captured-preview');
  const cameraDataInput = document.getElementById('camera_photo');

  let stream = null;

  if (openCamBtn) {
    openCamBtn.addEventListener('click', async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        camStream.srcObject = stream;
        camStream.play();
        camStream.style.display = 'block';
        capturedPrev.style.display = 'none';
        openCamBtn.style.display = 'none';
        captureBtn.style.display = 'inline-flex';
        if (closeCamBtn) closeCamBtn.style.display = 'inline-flex';
        if (retakeBtn) retakeBtn.style.display = 'none';
      } catch (err) {
        alert('Camera not available: ' + err.message);
      }
    });
  }

  if (captureBtn) {
    captureBtn.addEventListener('click', () => {
      const canvas = document.createElement('canvas');
      canvas.width = camStream.videoWidth;
      canvas.height = camStream.videoHeight;
      canvas.getContext('2d').drawImage(camStream, 0, 0);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
      cameraDataInput.value = dataUrl;

      capturedPrev.src = dataUrl;
      capturedPrev.style.display = 'block';
      camStream.style.display = 'none';
      captureBtn.style.display = 'none';
      if (closeCamBtn) closeCamBtn.style.display = 'none';
      if (retakeBtn) retakeBtn.style.display = 'inline-flex';

      // Stop stream
      if (stream) stream.getTracks().forEach(t => t.stop());
    });
  }

  if (retakeBtn) {
    retakeBtn.addEventListener('click', () => {
      cameraDataInput.value = '';
      capturedPrev.style.display = 'none';
      retakeBtn.style.display = 'none';
      openCamBtn.style.display = 'inline-flex';
    });
  }

  if (closeCamBtn) {
    closeCamBtn.addEventListener('click', () => {
      if (stream) stream.getTracks().forEach(t => t.stop());
      camStream.style.display = 'none';
      closeCamBtn.style.display = 'none';
      captureBtn.style.display = 'none';
      openCamBtn.style.display = 'inline-flex';
    });
  }

});
