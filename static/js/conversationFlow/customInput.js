var tied_target = ['', ''];
$('body').on('click','.tied-form-output', function(){
    tied_target[0] = $(this).attr('data-target');
    tied_target[1] = $(tied_target[0]).attr('data-target');
    console.log(tied_target);
    $(tied_target[0] ).focus();
    $(this).addClass('border');
    $(this).addClass('border-primary');
    $(tied_target[1]).html(processHTML($(tied_target[0]).val()));
});

$('body').on('keyup',tied_target[0], function(){
    console.log(tied_target);
    console.log($(tied_target[0]).val());
    $(tied_target[1]).html(processHTML($(tied_target[0]).val()));
});

$('body').on('focusout',tied_target[0], function(){
    console.log(tied_target);
    $(tied_target[1]).html(processHTML($(tied_target[0]).val(), false));
    $(tied_target[1]).removeClass('border');
    $(tied_target[1]).removeClass('border-primary');
    tied_target[0] = '';
    tied_target[1] = '';
});

function processHTML(raw_input, cursor=true){
    try{
        console.log(raw_input);
        var formatted_output = '';
        var curr_first = -1;
        var indices = [];
        var input_split = raw_input.split('');
        for(var i=0; i<input_split.length; i++){
            if(input_split[i] == '{'){
                curr_first = i
            }
            else if(input_split[i] == '}' && curr_first != -1){
                indices.push([curr_first, i])
                curr_first = -1;
            }
        }
        //console.log(indices);
        first_index = indices[0][0]
        first_part = raw_input.substring(0,first_index)
        formatted_output = first_part
        last_index = 0
        //console.log(formatted_output);
        for(var i=0; i<indices.length; i++){
            var indx = i;
            var indice = indices[i];
            first_index = indice[0];
            last_index = indice[1];
            try{
                value = '<span class="badge badge-success">' + raw_input.substring(first_index,last_index+1);
            }
            catch(error){
                value = raw_input.substring(first_index,last_index+1);
            }
            try{
                next_part = raw_input.substring(last_index+1,indices[indx+1][0])
            }
            catch(error){
                next_part = '</span>';
            }
            formatted_output += value+next_part
        }
        last_part = raw_input.substring(last_index+1,String(raw_input).length)
        formatted_output += last_part;
        console.log(cursor);
        if(cursor){
            formatted_output += '<span class="cursor">|</span>';
        }
        //console.log(formatted_output);
        return formatted_output;
    }catch(error){
        raw_input += '<span class="cursor">|</span>';
        console.log(raw_input);
        return raw_input;
    }
}