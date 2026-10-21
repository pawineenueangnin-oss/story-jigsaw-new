/* Change the game name here – used for the page title, loader and menu. */
window.GAME_CONFIG = {
  title: 'Moonpiece Tales',
  siteUrl: 'https://pawineenueangnin-oss.github.io/story-jigsaw-new/'
};
/* True inside the Moonpiece Android app (native bridges or UA marker). */
window.IS_ANDROID_APP = !!(window.AndroidApp || window.AndroidTTS || /\bMoonpieceApp\//.test(navigator.userAgent));
