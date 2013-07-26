function CMInstance(elem, options, events){
    if(!elem){
        return null;
    }

    var codemirrorObj = null;

    var defaults = {
        continuousScanning: 500,
        mode: 'htmlmixed',
        height: "40.2em",
        tabMode: "shift",
        indentUnit: 4,
        lineNumbers: true,
        lineWrapping: true,
        readOnly: true
    };

    //overwrite defaults if neccesary
    if(options){
        for(var j in options){
            if(options.hasOwnProperty(j)){
                defaults[j] = options[j];
            }
        }
    }

    //create CodeMirror instance
    codemirrorObj = CodeMirror.fromTextArea(elem, defaults);

    //attach events
    if(events instanceof Array ){
        for(var i=0; i<events.length; i++){
            if(typeof events[i]['handler'] === 'function'){
                codemirrorObj.on(events[i]['name'], events[i]['handler']);
            }
        }
    }

    return this;
}
