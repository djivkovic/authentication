import { SyntheticEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


const EditProfile = (props:{email:string, name:string, user_type:string}) => {
    const navigate = useNavigate();

    useEffect(() => {
        const timeout = setTimeout(() => {
            if (!props.name) {
                navigate('/login');
            }
        }, 1000);

        return () => clearTimeout(timeout);
    }, [props.name, navigate]);


    const [name, setName] = useState("");
    const editProfile = async (e: SyntheticEvent)=>{
        e.preventDefault();
        
        const uidb64 = localStorage.getItem("uidb64");

        if(name.length > 3){
            const response = await fetch(`http://localhost:8000/api/edit-profile/${uidb64}`,{
            method:"POST",
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({name})
        });

        if(response){
            alert('Successfully edited profile');
            window.location.reload();
        }
        else{
            alert("Error, try again...");
        }
        }else{

            alert("Something went wrong");
        }
       
    }


    return ( <div className="form-f form"><form onSubmit={editProfile}>
      <h1 className="h3 mb-3 font-weight-normal edit-title">Edit Profile</h1>
      <input type="text" className="form-control" name='name' placeholder={props.name} onChange={(e)=>{setName(e.target.value)}}></input>
      <input type="text" className="form-control" name='role' value={props.user_type} disabled></input>
      <input type="email" className="form-control email-input" value={props.email} disabled  />
      <button className="btn btn-lg btn-primary btn-block edit-btn" type="submit">Edit</button>
     </form></div>);
}
 
export default EditProfile;