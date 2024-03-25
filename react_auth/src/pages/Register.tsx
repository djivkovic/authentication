import { SyntheticEvent, useState } from "react";
import { useNavigate } from 'react-router-dom';


const Register = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [user_type, setUserType] = useState("");
    const navigate = useNavigate();

    const submit = async (e: SyntheticEvent)=>{
        e.preventDefault();

        const response = await fetch("http://localhost:8000/api/register",{
            method:"POST",
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({name, email, password,user_type})
        });

        const content = await response.json();

        navigate("/login")
    }

    return (  <form onSubmit={submit}>
      <h1 className="h3 mb-3 font-weight-normal">Please register</h1>
      <input type="text" className="form-control" placeholder="Name" name="name" required onChange={e => setName(e.target.value)}></input>
      <input type="email" className="form-control" placeholder="Email address" name="email" required onChange={e => setEmail(e.target.value)}></input>
      <input type="password" className="form-control" placeholder="Password" name="password" required onChange={e => setPassword(e.target.value)}/>
      <select className="form-control" onChange={(e)=>{
       setUserType(e.target.value);
      }} required>
                <option value="">Select user type</option>
                <option value="Guide">Guide</option>
                <option value="Tourist">Tourist</option>
                <option value="Administrator">Administrator</option>
                <option value="Accountant">Accountant</option>
                <option value="Moderator">Moderator</option>
            </select>
      <button className="btn btn-lg btn-primary btn-block" type="submit">Submit</button>
     </form>);
}
 
export default Register;