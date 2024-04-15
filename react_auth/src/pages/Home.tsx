import { Link } from "react-router-dom";

const Home = (props:{name:string, user_type:string}) => {
   
    return ( <><div>{props.name ? 'Hi ' + props.name + " " + (props.user_type) + '!': "You are not logged in..."}</div> 
    {props.user_type  ? <Link className="editProfile" to={'edit-profile'}>Edit Profile</Link> : ''}
    {props.user_type === "Accountant" ? (
    <a className="accounting-ms" href="http://localhost:3001/">
        Accountant MS
    </a>
    ) : null}
    </>);
}
export default Home;