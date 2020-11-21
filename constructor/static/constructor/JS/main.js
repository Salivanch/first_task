const anchors = document.querySelectorAll('a.scroll-to')

for (let anchor of anchors) {
    anchor.addEventListener('click', function (e) {
        e.preventDefault()
        
        const blockID = anchor.getAttribute('href')
        
        document.querySelector(blockID).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        })
    })
}


let form=document.querySelector(".question_form");
try{
    form.onsubmit=(e)=>{
        e.preventDefault();
        fetch(form.action,{
            method: "POST",
            body: new FormData(form),
        })
        .then(response => response.json())
        .then(function(json){
            console.log(json)
            if (json.status){
                console.log(form.querySelectorAll('input'))
                form.querySelectorAll('input').forEach(item=>item.value="")
            }
            else if (json.errors){
                for(let block of form.querySelectorAll('.errorlist'))
                    block.remove()
                if (json.errors.name){addError(json.errors.name, form.getElementsByTagName('p')[0])}
                if (json.errors.phone){addError(json.errors.name, form.getElementsByTagName('p')[1])}
                if (json.errors.email){addError(json.errors.email, form.getElementsByTagName('p')[2])}
            }
        })
        .catch(function(error){console.log(error)})
    }
}catch{}