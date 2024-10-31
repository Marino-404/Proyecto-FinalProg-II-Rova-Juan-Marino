let idx = 0;
const images = 2;

setInterval(() => {
  const currentImg = document.getElementById(`img${idx}`);
  currentImg.classList.toggle("main_image_show");
  currentImg.classList.toggle("main_image");

  idx++;

  if (idx > images) {
    idx = 0;
  }

  const nextImg = document.getElementById(`img${idx}`);
  nextImg.classList.toggle("main_image_show");
  nextImg.classList.toggle("main_image");
}, 4000);
