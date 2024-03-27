const Home = (props:{name:string, user_type:string}) => {
   
    return ( <><div>{props.name ? 'Hi ' + props.name + " " + (props.user_type) + '!': "You are not logged in..."}</div> 
    <button className="editProfile">Edit Profile</button></>);
}
 
export default Home;