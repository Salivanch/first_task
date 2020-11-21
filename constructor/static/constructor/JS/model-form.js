let modal=document.querySelector(".modal"),
    overlay=document.querySelector('.modal-overlay'),
    modal_open=document.querySelector('.open-modal'),
    modal_close=document.querySelector(".close-modal");

modal_open.onclick=()=>{
    modal.classList.add('active');
    overlay.classList.add('active');
    modal_open.style.display="none";
}

try{
    modal_close.onclick=()=>{
        modal.classList.remove('active');
        overlay.classList.remove('active');
        modal_open.style.display="block";
    }
}catch{}


let signin_form=document.querySelector('.signin'),
    signup_from=document.querySelector('.signup'),
    link=document.querySelector('.next');

try{
    signin_form.classList.add('activate');  
}catch{}

try{
    link.onclick=()=>{
        if (signup_from.classList.toggle('activate')){
            signin_form.classList.remove('activate');
            link.textContent="Есть аккаунт? Войти";
            signup_from.classList.add('activate');
            addHelp();
        }
        else{
            signin_form.classList.add('activate');
            link.textContent="Нет аккаунта? Зарегистрироваться";
            signup_from.classList.remove('activate');
            addHelp();
        }
    };
}catch{}

//Отправка запроса на авторизацию
try{
    signin_form.onsubmit=(e)=>{
        e.preventDefault();
        fetch(signin_form.action,{
            method: "POST",
            body: new FormData(signin_form),
        })
        .then(response => response.json())
        .then(function(json){
            if (json.link){
                window.location.href=json.link
            }
            else if (json.errors['__all__']){
                for(let block of signin_form.querySelectorAll('.errorlist'))
                    block.remove()
                addError(json.errors['__all__'], signin_form.getElementsByTagName('p')[0])
            }
            else{
                console.log(json)
            }
        })
        .catch(function(error){console.log(error)})
    }
}catch{}

//Отправка запроса на регистрацию
try{
    signup_from.onsubmit=(e)=>{
        e.preventDefault();
        fetch(signup_from.action,{
            method: "POST",
            body: new FormData(signup_from),
        })
        .then(response => response.json())
        .then(function(json){
            console.log(json)
            if (json.link){
                window.location.href=json.link
            }
            else if (json.errors){
                for(let block of signup_from.querySelectorAll('.errorlist'))
                    block.remove()
                removeHelp()
                if (json.errors.username){addError(json.errors.username, signup_from.getElementsByTagName('p')[0])}
                if (json.errors.password2){addError(json.errors.password2, signup_from.getElementsByTagName('p')[1])}
                if (json.errors.email){addError(json.errors.email, signup_from.getElementsByTagName('p')[4])}
            }
            else{
                console.log(json)
            }
        })
        .catch(function(error){console.log(error)})
    }
}catch{}

//добавление ошибки
const addError=(errors,insert)=>{
    let error_block='<ul class="errorlist">'
    for(let error of errors)
        error_block+=`<li>${error}</li>`;
    error_block+='</ul>';
    insert.insertAdjacentHTML("beforeend",error_block)
}

//очистка helptext, при errortext
const removeHelp=()=>{
    document.querySelectorAll('form .helptext').forEach(item=>{item.style.display="none"})
    document.querySelectorAll('form ul').forEach(item=>{item.style.display="none"})
}

//добавление helptext, при смене формы
const addHelp=()=>{
    document.querySelectorAll('form .helptext').forEach(item=>{item.style.display="block"})
    document.querySelectorAll('form ul').forEach(item=>{item.style.display="block"})
}