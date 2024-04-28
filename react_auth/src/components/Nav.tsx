import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const Nav = (props: { name: string; setName: (name: string) => void , setUserType:(userType:string)=>void, email: string; setEmail : (name:string)=>void, id: string; setId:(id:string)=>void}) => {
    const navigate = useNavigate();

    const logout = async () => {
        await fetch("http://localhost:8000/api/logout", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
        });

        props.setName("");
        localStorage.removeItem('isLoggedIn'); 
        navigate("/login");
    }

    useEffect(() => {
        const isLoggedIn = localStorage.getItem('isLoggedIn');
        if (isLoggedIn) {
            (
                async () => {
                    const response = await fetch("http://localhost:8000/api/user", {
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'include',
                    });

                    const content = await response.json();
                    console.log('content', content);
                    props.setUserType(content.user_type);
                    props.setName(content.name);
                    props.setEmail(content.email)
                    props.setId(content.id)
                }
            )();
        }
    }, [props.name]);

    let menu;
    if (!props.name) {
        menu = (
            <ul className="navbar-nav mr-auto">
                <li className="nav-item active">
                    <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item active">
                    <Link className="nav-link" to="/register">Register</Link>
                </li>
            </ul>
        )
    } else {
        menu = (
            <ul className="navbar-nav mr-auto">
                <li className="nav-item active">
                    <Link className="nav-link" to="/login" onClick={logout}>Logout</Link>
                </li>
            </ul>
        )
    }

    return (
        <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4">
            <Link className="navbar-brand" to="/">Home</Link>
            <div className="collapse navbar-collapse" id="navbarCollapse">
                {menu}
            </div>
        </nav>
    );
}

export default Nav;
