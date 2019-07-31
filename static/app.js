
window.addEventListener("load", function(){
  let vid = document.querySelector("video");
    
function playVid() { 
    vid.play();
    toggleFullscreen(); 
} 

function pauseVid() { 
    vid.pause(); 
} 

function toggleFullscreen() {
    let elem = document.querySelector("video");

    if (!document.fullscreenElement) {
    elem.requestFullscreen().catch(err => {
        alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
    });
    } else {
    document.exitFullscreen();
    }
}
});
        
