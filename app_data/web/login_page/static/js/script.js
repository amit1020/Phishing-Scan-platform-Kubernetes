sections_array = ["loginBx", "registration", "authentication","2FA_Verification_section"];

//For 2FA vertification
let USERNAME = undefined;
let USER_NAME_TO_ENTER = undefined

function Move_between_sections(sec){
    sections_array.forEach(function(item){
        if(item != sec){
            document.getElementById(item).style.display = "none";
        }else{
            document.getElementById(item).style.display = "block";
        }

        });

    };//! Close the function 




    


    //https://www.freecodecamp.org/news/how-to-send-http-requests-using-javascript/
    async function Send_Data_(data, url) {
        try {
            const response = await fetch(url, {
                method: "POST",
                body: data,
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",  //Ensures JSON encoding
                },
            });
    
            if (!response.ok) {
                throw new Error(`Network error: ${response.status} - ${response.statusText}`);
            }
    
            // Ensure the response is JSON
            const responseData = await response.json().catch(() => null);
            if (!responseData) throw new Error("Invalid JSON response from server");
    
            return responseData;
    
        } catch (error) {
            console.error("Fetch error:", error.message);
            return null;  // Always return null instead of crashing
        }
    }




    async function LoginFunction(){
        let url = `${window.location.origin}/api/UserLogin/`;
        console.log(url);
        USER_NAME_TO_ENTER = document.getElementById("login_username").value;
        let message_body = JSON.stringify({
            name: USER_NAME_TO_ENTER,
            password: document.getElementById("login_password").value
        });
        const permission = await Send_Data_(message_body, url);
        console.log(permission.status);

        if (permission && permission.status === "Success") {  
            Move_between_sections('authentication');
        } else {
            console.error("Not successful", permission.Error);
        }
        //TODO finish the route for the login
        //Move_between_sections('authentication')
    
    }
        


    
    async function VertifyOTP_UserLogin() {
        //The meaning of this line is to get the current URL of the page and add the path to the API
        let url = `${window.location.origin}/api/Vertification/2FA`;
        let message_body = JSON.stringify({
            username: USER_NAME_TO_ENTER,
            otp: document.getElementById("OTP_login").value
        });
        const response = await Send_Data_(message_body, url);
    
        if (response && response.status === "Success") {  
            window.location.href = response.redirect;  // Use Flask's redirect URL
        } else {
            console.error("Error");
        }
    }
    





    async function registration_function() {
        //The meaning of this line is to get the current URL of the page and add the path to the API
        let url = `${window.location.origin}/api/add_user/`;
        //Makes the USERNAME available globally
        USERNAME = document.getElementById("registration_username").value;
        let message_body = JSON.stringify({
            name: document.getElementById("registration_username").value,
            password: document.getElementById("registration_password").value,
            email: document.getElementById("registration_email").value,
            phone_number: document.getElementById("registration_phone_number").value
        });
        const response = await Send_Data_(message_body, url);
        if (response && response["2FA_key"]) {  
            Move_between_sections("2FA_Verification_section");
            document.getElementById("p_key").innerHTML = "Your key is: " + response["2FA_key"];
        } else {
            alert(response.Error);
            //console.error("Error:", response.Error);
        }
        Clear_registration();  
    }
    
    



    async function verify_otp() {
        //The meaning of this line is to get the current URL of the page and add the path to the API
        let url = `${window.location.origin}/api/Vertification/2FA`;
        let message_body = JSON.stringify({
            username: USERNAME,
            otp: document.getElementById("OTP_register").value
        });
        const response = await Send_Data_(message_body, url);
    
        if (response && response.status === "Success") {  
            window.location.href = response.redirect;  // Use Flask's redirect URL
            
        } else {
            console.error("Error");
        }
    }
    


//clear the registration form
function Clear_registration(){
    document.getElementById("registration_username").value = "";
    document.getElementById("registration_password").value = "";
    document.getElementById("registration_email").value = "";
    document.getElementById("registration_phone_number").value = "";
}


function Test(){
    console.log("Test");
}


