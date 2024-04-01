import { SyntheticEvent, useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { setuid } from "process";

const Login = (props: {name: string, setName: (name:string)=>void}) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [showResetModal, setShowResetModal] = useState(true);
    const [resetEmail, setResetEmail] = useState("");
    const [token, setToken] = useState("");
    const [uidb64, setUidb64] = useState("");
    const navigate = useNavigate();


    useEffect(() => {
            if (props.name) {
                navigate('/');
            }

    }, [props.name, navigate]);


   const openModal = () => {
        setShowModal(true);
    }

    const cookieString = Cookies.get("email-link");
    // console.log('Cookie: ', cookieString);

   const submit = async (e: SyntheticEvent) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const content = await response.json();
        props.setName(content.name);

        localStorage.setItem('isLoggedIn', 'true');
        navigate("/");
    } else {
        navigate("/login");
    }
}
useEffect(() => {
      if (token && uidb64) {
        localStorage.setItem('token', token);
        localStorage.setItem('uidb64', uidb64);
    }
}, [token, uidb64]);

const sendResetPasswordEmail = async (e: SyntheticEvent)=>{
    e.preventDefault();

    const response = await fetch("http://localhost:8000/api/request-reset-link",{
        method: "POST",
        headers: {'Content-Type':'application/json'},
        credentials: 'include',
        body: JSON.stringify({resetEmail})
    });

    if (response.ok){
        console.log("Reset email has been sent");
        setShowModal(false);
        const data = await response.json();
        setToken(data.token);
        setUidb64(data.uidb64);
        alert("Reset email has been sent, once you open link you will need to refresh page")
    }
}

const resetPassword = async (e:SyntheticEvent)=>{
    e.preventDefault();

    if(newPassword !== confirmNewPassword){
        console.log("Password must match!");
        return;
    }
    const ls_token = localStorage.getItem('token');
    const ls_uidb64 = localStorage.getItem('uidb64')
    const response = await fetch(`http://localhost:8000/api/set-new-password/${ls_uidb64}/${ls_token}`,{
        method: "POST",
        headers: {'Content-Type':'application/json'},
        credentials: 'include',
        body: JSON.stringify({newPassword, confirmNewPassword})
    });

    if (response.ok){
        console.log("Password successfully changed");
        alert( "Your password has been updated" );
        setShowResetModal(false);
        localStorage.removeItem("token");
        localStorage.removeItem("uidb64");
        Cookies.remove("email-link");
    }
}



    return ( <><div className="form-f form"><form onSubmit={submit}>
      <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
      <input type="email" name="email" className="form-control" placeholder="Email address" onChange={e => setEmail(e.target.value)} required></input>
      <input type="password" name="password" className="form-control password-input" placeholder="Password" onChange={e => setPassword(e.target.value)} required/>
      <button className="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
     </form> 
     <button className="forgot-password" onClick={openModal}>Forgot password?</button>
     </div>

     {showModal && (
                <div className="container">
            <div className="wrapper">
                               <span className="close-icon" onClick={()=>setShowModal(false)} >
              &times;
            </span>
                <form className="form">
                    <label>Enter email to send link for password reset</label>
                    <input placeholder="Your email..." onChange={e => setResetEmail(e.target.value)} name="resetEmail"></input>
                    <button onClick={sendResetPasswordEmail}>Send Email</button>
                </form>
            </div>
    </div>
            )}
       {showResetModal && cookieString && (
                <div className="container">
            <div className="wrapper">
                               <span className="close-icon" onClick={()=>setShowResetModal(false)} >
              &times;
            </span>
                <form className="form">
                    <label>Enter your new password</label>
                    <input type="password" placeholder="Your password" onChange={e => setNewPassword(e.target.value)} name="newPassword"></input>
                     <input type="password" placeholder="Confirm your password" onChange={e => setConfirmNewPassword(e.target.value)} name="confirmNewPassword"></input>
                    <button onClick={resetPassword}>Reset Password</button>
                </form>
            </div>
    </div>
            )}
     </>
     );
}
 
export default Login;