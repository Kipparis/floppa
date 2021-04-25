cross = new Image();
cross.src = document.getElementById('file2').value;

// cross.src = '..'

files_arr = JSON.parse(document.getElementById('file1').value); //arr for path and flag
// files_arr =
curr_idx = files_arr.current_idx;
paths = files_arr.paths;

base_image = new Image();
base_image.src = paths[curr_idx];

var index_of_max = document.getElementById('counter');
index_of_max.value = curr_idx.toString() + '/' + (paths.length-1).toString();

function make_base() {
    var canvas = document.getElementById('canvas'),
    context = canvas.getContext('2d');
    base_image = new Image();
    base_image.src = base_image_name;
    base_image.onload = function() {
        canvas.width = base_image.width;
        canvas.height = base_image.height;
        document.getElementById('pic_box').style.height = base_image.height + 'px';
        context.drawImage(base_image, 0, 0);
    }
}
make_base();

let isDrawing = false;
let x = 0, y = 0, mode = 'to_draw', razmetka = []
const myPics = document.getElementById('canvas');
const context = myPics.getContext('2d');

myPics.addEventListener('mousedown', e => {
    if (mode === 'to_draw') {
        x = e.offsetX;
        y = e.offsetY;
        isDrawing = true;
    }
});

myPics.addEventListener('mousemove', e => {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    context.beginPath();
    context.drawImage(base_image, 0, 0);
    if (paths[curr_idx] in razmetka) {
        var raz_p = razmetka[paths[curr_idx]]
        for (var i = 0; i < raz_p.length; i++) {
            context.strokeRect(raz_p[i].x1, raz_p[i].y1, raz_p[i].x2-raz_p[i].x1, raz_p[i].y2-raz_p[i].y1);
        }
    }
    if (isDrawing === true) {
        context.strokeRect(x, y, e.offsetX-x, e.offsetY-y);
    } else if (mode === 'to_delete') {
        if (paths[curr_idx] in razmetka) {
            var raz_p = razmetka[paths[curr_idx]]
            for (var i = 0; i < razmetka.length; i++) {
                context.drawImage(cross, raz_p[i].x2, raz_p[i].y1-40);
            }
        }
    }
});

window.addEventListener('mouseup', e => {
    if (isDrawing === true) {
        isDrawing = false;
        tag = document.getElementById('defect_option').value;
        if (tag != '') {
            if (paths[curr_idx] in razmetka) {
                if (y > e.offsetY && x > e.offsetX) {
                    razmetka[paths[curr_idx]].push({tag:tag,x1:e.offsetX,y1:e.offsetY,x2:x,y2:y})
                } else if (y > e.offsetY) {
                    razmetka[paths[curr_idx]].push({tag:tag,x1:x,y1:e.offsetY,x2:e.offsetX,y2:y})
                } else if (x > e.offsetX) {
                    razmetka[paths[curr_idx]].push({tag:tag,x1:e.offsetX,y1:y,x2:x,y2:e.offsetY})
                } else {
                    razmetka[paths[curr_idx]].push({tag:tag,x1:x,y1:y,x2:e.offsetX,y2:e.offsetY})
                }
            }
        }
        console.log(razmetka)
    } else if (mode === 'to_delete') {
        if (paths[curr_idx] in razmetka) {
            var raz_p = razmetka[paths[curr_idx]]
            for (var i = 0; i < raz_p.length; i++) {
                if (e.offsetX < raz_p[i].x2+40 && e.offsetX > raz_p[i].x2 && e.offsetY < raz_p[i].y1 && e.offsetY > raz_p[i].y1-40) {
                    razmetka[paths[curr_idx]].splice(i,1);
                    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
                    context.beginPath();
                    context.drawImage(base_image, 0, 0);
                    for (var i = 0; i < razmetka.length; i++) {
                        context.strokeRect(raz_p[i].x1, raz_p[i].y1, raz_p[i].x2-raz_p[i].x1, raz_p[i].y2-raz_p[i].y1);
                        context.drawImage(cross, raz_p[i].x2, raz_p[i].y1-40);
                    }
                    break
                }
            }
        }
    }
});

function to_draw() {
    mode = 'to_draw';
}

function to_delete() {
    mode = 'to_delete';
}

function prev_picture() {
    if (curr_idx > 0) {
        curr_idx -= 1;
        base_image = new Image();
        base_image.src = paths[curr_idx];
        var index_of_max = document.getElementById('sasha');
        index_of_max.value = curr_idx.toString() + '/' + (paths.length-1).toString();
    }
}

function next_picture() {
    if (curr_idx < paths.length - 1) {
        curr_idx += 1;
        base_image = new Image();
        base_image.src = paths[curr_idx];
        var index_of_max = document.getElementById('sasha');
        index_of_max.value = curr_idx.toString() + '/' + (paths.length-1).toString();
    }
}

function to_save() {
    var json = JSON.stringify([base_image_name, razmetka]);
    var res = document.getElementById('hidden_input');
    res.value = json;
    console.log(res.value);
    // json = [json];
    // var blob1 = new Blob(json, { type: "text/plain;charset=utf-8" });
    // var url = window.URL || window.webkitURL;
    // link = url.createObjectURL(blob1);
    // var a = document.createElement("a");
    // a.download = base_image_name+'.json';
    // a.href = link;
    // document.body.appendChild(a);
    // a.click();
    // document.body.removeChild(a);
}
