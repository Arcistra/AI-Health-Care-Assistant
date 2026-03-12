function validateForm() {
    let name = document.forms["appointmentform"]["Your_Name"].value;
    let age = document.forms['appointmentform']['Age'].value;
    let disease = document.forms['appointmentform']['Disease'].value;
    let doctor_selection = document.forms['appointmentform']['Doctor'].value;

    if (name == "" && name.length >= 3) {
      prompt("Name must be filled out");
      return false;
    }
    else if (disease == ''){
        alert("Disease must be filled out");
        return false;
    }
    else if (age == '' && age == String){
        alert("Age must be filled out");
        return false;
    }
    else if (doctor_selection.Select = none){
        alert("Select the Doctor Must");
        return false;
    }
  }