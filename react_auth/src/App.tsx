import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './pages/Login';
import Nav from './components/Nav';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Register from './pages/Register';

function App() {
  const [name, setName] = useState("");
  const [user_type, setUserType] = useState("");

 
  return (
    <div className="App">
       <BrowserRouter>
          <Nav name={name} setName={setName} setUserType={setUserType}/>
        <main className='form-signin'>
        <Routes>
          <Route path='/' element={<Home name={name} user_type={user_type}/>}/>
          <Route path='/login' element={<Login name={name} setName={setName}/>}/>
          <Route path='/register' element={<Register />}/>
        </Routes>
        </main>
      </BrowserRouter>
    </div>
  );
}

export default App;
