let idx = 0;
const images = 2;

setInterval(() => {
  const currentImg = document.getElementById(`img${idx}`);

  currentImg.classList.remove("slide-in-right");
  currentImg.classList.add("slide-out-left");
  currentImg.classList.remove("main_image_show");
  currentImg.classList.add("main_image");

  idx++;

  if (idx > images) {
    idx = 0;
  }

  const nextImg = document.getElementById(`img${idx}`);

  nextImg.classList.remove("slide-out-left");
  nextImg.classList.add("slide-in-right");
  nextImg.classList.remove("main_image");
  nextImg.classList.add("main_image_show");
}, 4000);
