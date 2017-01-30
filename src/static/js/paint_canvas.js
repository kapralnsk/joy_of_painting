var palette = $('#palette');
var brush_picker = $('#brush');
var canvas_elt = $('#canvas');
var canvas = canvas_elt[0];
var context = canvas.getContext("2d");
var brush = 8;
context.lineCap="round";
context.lineWidth = brush;
var color = "#000000";
var currentPoint={x:0, y:0}, previousPoint={x:0, y:0}
var mousePressed = false;

palette.spectrum({
    color: color,
    change: setColor
});
brush_picker.dropdown();
brush_picker.change(setBrushSize);

$("#save").click(save);
$('#clear').click(clear);

var image_id = window.location.pathname.split('/').slice(-1)[0];
if (!!image_id){
    canvas_elt.attr('image_id', image_id);
    image = $.get({
        url: '/image/' + image_id,
        success: loadImage
    })
}

function loadImage(data, textStatus, jqXHR){
    image = new Image();
    image.onload = function(){
        context.drawImage(image, 0, 0)
    }
    image.src = data['image']
}

function draw() {
    if (mousePressed) {
        context.beginPath();
        context.strokeStyle = color;
        context.moveTo(previousPoint.x, previousPoint.y);
        context.lineTo(currentPoint.x, currentPoint.y);
        context.stroke();
        context.closePath();
    }
    previousPoint={x:currentPoint.x, y:currentPoint.y};
}

function setColor(newColor){
    color = newColor.toHexString()
}

function setBrushSize(event){
    context.lineWidth = parseInt($(event.target).val())
}

function setCoords(x,y){
    currentPoint = {x:x, y:y};
}

canvas.onmousedown=function(){
    setCoords(event.offsetX,event.offsetY)
    draw();
    mousePressed = true;
}

document.body.onmouseup=function(){
    mousePressed = false;
}

canvas.onmousemove=function(){
    setCoords(event.offsetX,event.offsetY)
    if(mousePressed)
        draw();
}

function handle_save(data, textStatus, jqXHR){
    image_id = data['id']
    canvas_elt.attr('image_id', image_id)
    $('#image_link').attr('href', window.location.origin + '/gallery/' + image_id)
    $('#image_link').text(window.location.origin + '/gallery/' + image_id)
    $('#save-modal').modal('show');
}

function clear(){
    context.clearRect(0,0,canvas.width, canvas.height);
    if (!!image_id){
        canvas_elt.attr('image_id', '')
    }
}

function save(){
    image = canvas.toDataURL('image/png');
    if (!!canvas_elt.attr('image_id')){
        $.ajax({
        url: 'image/' + canvas_elt.attr('image_id'),
        type: 'PUT',
        data: {image: image},
        success: handle_save,
        dataType: 'json'
        })
    }
    else {
        $.post(
            'image/',
            {image: image},
            handle_save
        )
    }
}
