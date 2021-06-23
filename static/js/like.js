const btn = document.querySelector('#like_btn');


let like = true,
  likeCount = document.querySelector('.likes').innerHTML;
btn.addEventListener('click', like_handler);

function like_handler(e) {
	likeCount = like ? ++likeCount : --likeCount;
    like = !like;
    document.querySelector('.likes').innerHTML = likeCount;
}