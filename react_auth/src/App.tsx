import  {  useState } from 'react';
import './App.css';
import Login from './pages/Login';
import Nav from './components/Nav';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Register';
import CompleteResetPassword from './pages/CompleteResetPassword';
import EditProfile from './pages/EditProfile';


function App() {
  const [name, setName] = useState("");
  const [user_type, setUserType] = useState("");
  const [email, setEmail] = useState("");

 
  return (
    <div className="App">
       <BrowserRouter>
          <Nav name={name} setName={setName} setUserType={setUserType} email={email} setEmail={setEmail}/>
        <main className='form-signin'>
        <Routes>
          <Route path='/' element={<Home name={name} user_type={user_type}/>}/>
          <Route path='/login' element={<Login name={name} setName={setName}/>}/>
          <Route path='/register' element={<Register />}/>
          <Route path='/edit-profile' element={<EditProfile name={name} user_type={user_type}  email={email}/>}/>
          <Route path='/complete-reset-password' element={<CompleteResetPassword />}/>
        </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
