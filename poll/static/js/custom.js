$(document).ready(function(){
    $(".write-post-box").click(function(){
      $(".post-popup-box").show();
    });
    $(".close-post-box").click(function(){
        $(".post-popup-box").hide();
      });
      $(".setting-dropdown").click(function(){
        $(".profile-setting").toggle();
      });
      $(".show-hide-chat").click(function(){
        $(".chat-box-body").toggle();
      });
      $(".like-react").mouseover(function(){
        $(".reaction-emoji-box").show();
        
      });
      $(".like-react").mouseleave(function(){
          setTimeout(function(){
            $('.reaction-emoji-box').hide();
          }, 2000);
      });
  });