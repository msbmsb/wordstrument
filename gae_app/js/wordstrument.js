function playMusic(midiUrl) {
  stopMusic();
  $('body').append('<embed src="' + midiUrl + '" id="midi" autostart="true" class="offscreen"/>');
}

function stopMusic() {
  $('#midi').remove();
}

function makeUrl(notes) {
  var shorterNotes = notes.replace(/\s/g, "");
  return "midi?n=" + escape(notes);
}

function readField(id) {
  return $('#' + id).val();
}
