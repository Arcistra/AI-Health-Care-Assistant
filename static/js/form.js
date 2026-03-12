function validate() {
    let name = document.forms['signup_form']['fname'].value;
    let lname = document.forms['signup_form']['lname'].value;
    let pnumber = document.forms['signup_form']['pnumber'].value;
    let state = document.forms['signup_form']['state'].value;
    let city = document.forms['signup_form']['city'].value;
    let Address = document.forms['signup_form']['Address'].value;
    let eml = document.forms['signup_form']['eml'].value;
    mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    let Password = document.forms['signup_form']['Password'].value;
    let Confirm_Password = document.forms['signup_form']['Confirm_Password'].value;
    

    if (name == "" || name == null)
    {
            document.forms['signup_form']['fname'].style.border = "2px solid red";
            document.forms['signup_form']['fname'].values = " ";
    }
    else if (lname == "" || lname == null)
    {
            document.forms['signup_form']['lname'].style.border = "2px solid red";
            document.forms['signup_form']['lname'].innerText = "";
    }
    else if (pnumber.length < 11 || pnumber > 13 || pnumber == null)
    {
            document.forms['signup_form']['pnumber'].style.border = "2px solid red";
            document.forms['signup_form']['pnumber'].innerText = "";
    }
    else if (state == "" || state == null)
    {
            document.forms['signup_form']['state'].style.border = "2px solid red";
            document.forms['signup_form']['state'].innerText = "";
    }
    else if (city == "" || city == null)
    {
            document.forms['signup_form']['city'].style.border = "2px solid red";
            document.forms['signup_form']['city'].values = " ";
    }
    else if (Address == "" || Address == null)
    {
            document.forms['signup_form']['Address'].style.border = "2px solid red";
            document.forms['signup_form']['Address'].values = " ";
    }
    else if (eml == "" || !eml.match(mailformat))
    {
            document.forms['signup_form']['eml'].style.border = "2px solid red";
            document.forms['signup_form']['eml'].values = " ";
    }
    else if (Password == "" || Password.length < 8)
    {
            document.forms['signup_form']['Password'].style.border = "2px solid red";
            document.forms['signup_form']['Password'].values = " ";
    }
    else if (Confirm_Password != Password)
    {
            document.forms['signup_form']['Confirm_Password'].style.border = "2px solid red";
            document.forms['signup_form']['Confirm_Password'].values = " ";
    }
    else
    {
        console.log("successfully entered")
    }
}