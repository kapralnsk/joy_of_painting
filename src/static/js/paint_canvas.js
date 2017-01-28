var palette = $('#palette');
var canvas_elt = $('#canvas')
var canvas = canvas_elt[0];
var context = canvas.getContext("2d");

var currentPoint={x:0, y:0}, previousPoint={x:0, y:0}

var mousePressed = false;

var color = "#000000";

$("#save").click(save);

context.lineCap="round";
context.lineWidth = 8;

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
    canvas_elt.attr('image_id', data['id'])
    $('#save-modal .content').text(window.location.origin + '/gallery/' + data['id'])
    $('#save-modal').modal('show');
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
