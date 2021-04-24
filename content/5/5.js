make_base();

function make_base() {
    var canvas = document.getElementById('canvas'),
    context = canvas.getContext('2d');
    base_image = new Image();
    base_image.src = '../pic/cat.jpg';

    base_image.onload = function() {
        canvas.width = base_image.width;
        canvas.height = base_image.height;
        document.getElementById('pic_box').style.height = base_image.height + 'px';
        context.drawImage(base_image, 0, 0);
        // console.log(base_image.width, base_image.height);
        // console.log(document.getElementById('pic_box').style.width, document.getElementById('pic_box').style.height);
    }
}



let isDrawing = false;
let x = 0;
let y = 0;
let mode = 'to_draw'

var razmetka = []

const myPics = document.getElementById('canvas');
const context = myPics.getContext('2d');

base_image_name = '../pic/cat.jpg';
base_image = new Image();
base_image.src = base_image_name;

cross = new Image();
cross.src = '../pic/cross.png';

myPics.addEventListener('mousedown', e => {
    if (mode === 'to_draw') {
        x = e.offsetX;
        y = e.offsetY;
        isDrawing = true;
    }
});

myPics.addEventListener('mousemove', e => {
    if (isDrawing === true) {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        context.beginPath();
        context.drawImage(base_image, 0, 0);
        for (var i = 0; i < razmetka.length; i++) {
            context.strokeRect(razmetka[i].x1, razmetka[i].y1, razmetka[i].x2-razmetka[i].x1, razmetka[i].y2-razmetka[i].y1);
        }
        context.strokeRect(x, y, e.offsetX-x, e.offsetY-y);
    } else if (mode === 'to_delete') {
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
        context.beginPath();
        context.drawImage(base_image, 0, 0);
        for (var i = 0; i < razmetka.length; i++) {
            context.strokeRect(razmetka[i].x1, razmetka[i].y1, razmetka[i].x2-razmetka[i].x1, razmetka[i].y2-razmetka[i].y1);
            context.drawImage(cross, razmetka[i].x2, razmetka[i].y1-40);
        }
    }
});

window.addEventListener('mouseup', e => {
    if (isDrawing === true) {
        // drawLine(context, x, y, e.offsetX, e.offsetY);
        isDrawing = false;
        tag = document.getElementById('defect_option').value;
        if (tag != '') {
            if (y > e.offsetY && x > e.offsetX) {
                razmetka.push({tag:tag,x1:e.offsetX,y1:e.offsetY,x2:x,y2:y})
            } else if (y > e.offsetY) {
                razmetka.push({tag:tag,x1:x,y1:e.offsetY,x2:e.offsetX,y2:y})
            } else if (x > e.offsetX) {
                razmetka.push({tag:tag,x1:e.offsetX,y1:y,x2:x,y2:e.offsetY})
            } else {
                razmetka.push({tag:tag,x1:x,y1:y,x2:e.offsetX,y2:e.offsetY})
            }
        }
        console.log(razmetka)
    } else if (mode === 'to_delete') {
        for (var i = 0; i < razmetka.length; i++) {
            if (e.offsetX < razmetka[i].x2+40 && e.offsetX > razmetka[i].x2 && e.offsetY < razmetka[i].y1 && e.offsetY > razmetka[i].y1-40) {
                razmetka.splice(i,1);
                context.clearRect(0, 0, context.canvas.width, context.canvas.height);
                context.beginPath();
                context.drawImage(base_image, 0, 0);
                for (var i = 0; i < razmetka.length; i++) {
                    context.strokeRect(razmetka[i].x1, razmetka[i].y1, razmetka[i].x2-razmetka[i].x1, razmetka[i].y2-razmetka[i].y1);
                    context.drawImage(cross, razmetka[i].x2, razmetka[i].y1-40);
                }
                break
            }
        }
    }
});

function to_draw() {
    mode = 'to_draw';
    console.log(mode)
}

function to_delete() {
    mode = 'to_delete';
    console.log(mode)
}

function to_save() {
    var json = JSON.stringify([base_image_name, razmetka])
    // saveAs(json, base_image_name+'.json');
    //
    json = [json];
    var blob1 = new Blob(json, { type: "text/plain;charset=utf-8" });

    var url = window.URL || window.webkitURL;
    link = url.createObjectURL(blob1);
    var a = document.createElement("a");
    a.download = base_image_name+'.json';
    a.href = link;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// var json = JSON.stringify(customers);
//
// //Convert JSON string to BLOB.
// json = [json];
// var blob1 = new Blob(json, { type: "text/plain;charset=utf-8" });
//
// //Check the Browser.
// var isIE = false || !!document.documentMode;
// if (isIE) {
//     window.navigator.msSaveBlob(blob1, "Customers.txt");
// } else {
//     var url = window.URL || window.webkitURL;
//     link = url.createObjectURL(blob1);
//     var a = document.createElement("a");
//     a.download = "Customers.txt";
//     a.href = link;
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
// }

// function drawLine(context, x1, y1, x2, y2) {
//     context.beginPath();
//     context.strokeStyle = 'black';
//     context.lineWidth = 1;
//     context.moveTo(x1, y1);
//     context.lineTo(x2, y2);
//     context.stroke();
//     context.closePath();
// }


// compress(e) {
//   const width = 500;
//   const height = 300;
//   const fileName = e.target.files[0].name;
//   const reader = new FileReader();
//
//   reader.readAsDataURL(e.target.files[0]);
//   reader.onload = event => {
//     const img = new Image();
//     img.src = event.target.result;
//     img.onload = () => {
//       const elem = document.createElement('canvas');
//       elem.width = width;
//       elem.height = height;
//       const ctx = elem.getContext('2d');
//       // img.width и img.height будет содержать оригинальные размеры
//       ctx.drawImage(img, 0, 0, width, height);
//       ctx.canvas.toBlob((blob) => {
//         const file = new File([blob], fileName, {
//           type: 'image/jpeg',
//           lastModified: Date.now()
//         });
//       }, 'image/jpeg', 1);
//     };
//     reader.onerror = error => console.log(error);
//   };
// }
