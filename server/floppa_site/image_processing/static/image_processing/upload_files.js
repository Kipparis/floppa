let dropArea = document.getElementById('drop-area')
// dropArea.addEventListener('dragenter', handlerFunction, false)
// dropArea.addEventListener('dragleave', handlerFunction, false)
// dropArea.addEventListener('dragover', handlerFunction, false)
// dropArea.addEventListener('drop', handlerFunction, false)

function highlight(e) {
  dropArea.classList.add('highlight')
}
function unhighlight(e) {
  dropArea.classList.remove('highlight')
}
function preventDefaults (e) {
  e.preventDefault()
  e.stopPropagation()
}

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false)
})
;['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false)
})
;['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false)
})


dropArea.addEventListener('drop', handleDrop, false)
function handleDrop(e) {
  let dt = e.dataTransfer
  let files = dt.files
  handleFiles(files)
  console.log('files dropped')
}

function previewFile(file) {
  let reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onloadend = function() {
    let img = document.createElement('img')
    img.src = reader.result
    document.getElementById('gallery').appendChild(img)
  }
}

// let filesDone = 0
// let filesToDo = 0
// let progressBar = document.getElementById('progress-bar')
// function progressDone() {
//   filesDone++
//   progressBar.value = filesDone / filesToDo * 100
// }

function handleFiles(files) {
  files = [...files]
  initializeProgress(files.length) // <- Добавили эту строку
  files.forEach(uploadFile)
  files.forEach(previewFile)
}

let uploadProgress = []

function initializeProgress(numFiles) {
  // progressBar.value = 0
  uploadProgress = []
  for(let i = numFiles; i > 0; i--) {
    uploadProgress.push(0)
  }
}

// function updateProgress(fileNumber, percent) {
//   uploadProgress[fileNumber] = percent
//   let total = uploadProgress.reduce((tot, curr) => tot + curr, 0) / uploadProgress.length
//   progressBar.value = total
// }

var handled_img = []

function uploadFile(file, i) {
  handled_img.push(file)
  console.log('files handled')
  console.log(file)
}

function handle_data() {
    if (handled_img.length != 0) {
        document.getElementById('drop-area').style.display = 'none';
        document.getElementById('pic_box').style.display = 'block';
        // var preview = document.querySelector('img');
        // var file    = document.querySelector('input[type=file]').files[0];
        var file = handled_img[0]
        var reader  = new FileReader();
        var canvas = document.getElementById('canvas'),
        context = canvas.getContext('2d');
        var preview = new Image();
        reader.onloadend = function () {
          preview.src = reader.result;
          canvas.width = preview.width;
          canvas.height = preview.height;
          document.getElementById('pic_box').style.height = preview.height + 'px';
          context.drawImage(preview, 0, 0);
          console.log('loaded')
        }
        // Read in the image file as a data URL.
        reader.readAsDataURL(file);
        reader.onload = function(evt){
            if (evt.target.readyState == FileReader.DONE) {
                preview.src = evt.target.result;
                canvas.width = preview.width;
                canvas.height = preview.height;
                document.getElementById('pic_box').style.height = preview.height + 'px';
                context.drawImage(preview,0,0);
            }
            console.log('loaded2')
        }
    }
}
