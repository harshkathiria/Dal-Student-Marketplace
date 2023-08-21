import * as React from "react";
import { Link} from 'react-router-dom';

import logo from '../../assets/logo.png';
import {login} from '../../services/api-service'
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Form() {

  let credentials = {
    username: '',
    password: ''
  };

  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});

  const handleSubmit = (event) => {
    event.preventDefault();
    const errors = {};
    if (!username.endsWith('@dal.ca')) {
      errors.username = 'Dal email is required';
    }
    if (!password) {
      errors.password = 'Password is required';
    }
    if (Object.keys(errors).length > 0) {
      setErrors(errors);
    } else {
      credentials = {
        username: username,
        password: password
      }
      console.log(credentials);
      login(credentials)
        .then((response) => {
          console.log(response.data);
          const token = response.data.token;
          localStorage.setItem("token", token);
          navigate('/WelcomePage');
        })
        .catch((error) => {
          console.log(error);
          if (error.response && error.response.status === 400) {
            setErrorMessage('Incorrect password. Please try again.');
          }
        });
    }
  }
  function handleEmailChange(event) {
    setUsername(event.target.value);
    setErrors({});
  }

  function SignUp() {
    navigate('/SignUp');
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
    setErrors({});
  };

  return (
    <div className="bg-white w-full h-screen pt-4">

      <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 font-extrabold">Student Marketplace </h2>
      <hr/>

      <div className="user_nav">
        <div class="relative inline-block">
        <Link to="/"><b>&nbsp;&nbsp;Home&nbsp;&nbsp;</b></Link>
        </div>
      </div>

      <div className="pl-5">
        <p className="font-bold text-2xl pb-1 text-black mt-2">
        <h2 className="text-2xl font-semibold">Welcome!</h2>
        </p>
      </div>
      
      <div className="bg-white px-popup pt-10 mb-28 pb-h">

        <h2 className="text-2xl font-semibold text-gray-500">Login</h2>
        
        <div className="mt-8">
          <div>
            <label className="text-lg font-medium">Username</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-4 mt-1 bg-transparent italic"
              placeholder="example@dal.ca"
              value={username} 
              /*onChange={e => setUsername(e.target.value)}*/
              onChange={handleEmailChange}
            />
            {errors.username && <p className="text-red-500 italic ">{errors.username}</p>}
          </div>

          <div className="pt-3">
            <label className="text-lg font-medium">Password</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-4 mt-1 bg-transparent italic"
              placeholder="password"
              type={"password"}
              value={password} 
              /*onChange={e => setPassword(e.target.value)}*/
              onChange={handlePasswordChange}
            />
            {errors.password && <span>{errors.password}</span>}
            <div className="mt-4 text-red-500 italic">{errorMessage}</div>  
          </div>
          

          <div className="mt-8 flex flex-col gap-y-4">
            <button type="submit" onClick={handleSubmit} className="active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-bold">
              Login
            </button>
          </div>

          <div className=" flex justify-center items-center mt-4">
            {/* <button className="italic font-medium text-base hover:underline decoration-[2px] decoration-[#FFD400]">
              Forgot your password?
            </button>
            &nbsp;&nbsp;| */}
            <button type="button" onClick={SignUp} className="italic font-medium text-base hover:underline decoration-[2px] decoration-[#FFD400] ml-2">
              Don't have an account? SignUp
            </button>  
          </div>
        </div>
      </div>

      <hr/>
      <div className="footer">
        <div className='footer_text1'>
          <b>Dalhousie University</b><br/>Halifax, Nova Scotia, Canada B3H 4R2
        </div>

        <div className='footer_text2'>
          <Link className="footer_links" to="">&nbsp;About&nbsp;</Link>
          <Link className="footer_links" to="">&nbsp;Contact Us&nbsp;</Link>         
        </div>
      </div>   
    </div>
  );
}















