// function reveal(){
//     // Find the element
//          x=document.getElementsByClassName();
//     //Option 1: Change the style attribute directly
//           x.style.display="block";
    
//     //Option 2: Change the class which calls the CSS therefore, doing the same as above
//           // x.className="open";
//   }



function imgError(image) {
      image.onerror = "";
      image.src = "../static/images/non_pic.png";
      
      return true;
  }


// meant to reveal the images but due to loading factors, 
  function imgshow() {
      document.getElementsByClassName("before_image")[0].style.display = "none";
      document.getElementById("after_image").style.display = "none";

  }