import { SyntheticEvent, useState } from "react";
import { useNavigate } from 'react-router-dom';

const Login = (props: {name: string, setName: (name:string)=>void}) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

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

    return (  <form onSubmit={submit}>
      <h1 className="h3 mb-3 font-weight-normal">Please sign in</h1>
      <input type="email" name="email" className="form-control" placeholder="Email address" onChange={e => setEmail(e.target.value)} required></input>
      <input type="password" name="password" className="form-control" placeholder="Password" onChange={e => setPassword(e.target.value)} required/>
      <button className="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
     </form> );
}
 
export default Login;