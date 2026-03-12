function sendEmail(email_address) {
    rznd_number = Math.floor(100000 + Math.random() * 900000)
    Email.send({
        Host : "smtp.elasticemail.com",
        Username : "Mirfaizanali78@gmail.com",
        Password : "60AE0186092B259729C3EBA149587A947C88",
        To : email_address,
        From : "mirfaizanali78@gmail.com",
        Subject : "Reset Code for AI Healthcare",
        Body : `Dear ,

        We have received your request for a reset code for your AI healthcare account. Your reset code for `+email_address+` is: `+rand_number+`.
        
        Please use this code to reset your password on the "Reset Password" page and follow the prompts to create a new password for your account.
        
        If you have any trouble with this process, please do not hesitate to reach out to our customer support team for assistance.
        
        Thank you for using our AI healthcare service.
        
        Best,
        AI Healthcare Team`,
                 
    })
}
function varify() {
    email = document.forms['reset_form']('email').value
    console.log(Math.floor(100000 + Math.random() * 900000))
    mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    // sendEmail()
    if (!email.match(mailformat)) {
        document.getElementById("alertss").style.display = "flex"
        document.getElementById("alertss").innerHTML = "Invalid Email!"
    }
    else {
        sendEmail(email);
        document.getElementById("alerts").style.display = "flex"
        document.getElementById("alerts").innerHTML = "Successfully Reset Passsword"
    }
}

