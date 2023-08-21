// import * as React from "react";
import { Link } from 'react-router-dom';
import React, { useState } from "react";
import logo from '../../assets/logo.png';
// import axios from 'axios';
import {signup} from '../../services/api-service'
import {verify_email} from '../../services/api-service';
import { Button, Form, Modal } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

export default function SignupForm() {

  const [showOtpModal, setShowOtpModal] = useState(false);
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();

  let user = {
    name: '',
    email: '',
    password: '',
    phone: '',
    address:'',
    postalcode:''
  };

  let otp_verification = {
    username : '',
    otp : ''
  }
  const [errorMessage, setErrorMessage] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [postalcode, setPostalcode] = useState('');
  const [isEmailValid, setIsEmailValid] = useState(false);
  const [isPasswordValid, setIsPasswordValid] = useState(false);
  
  function handleEmailChange(event) {
    const newEmail = event.target.value;
    setEmail(newEmail);
    setIsEmailValid(newEmail.endsWith('@dal.ca'));
  }

  function handlePasswordChange(event) {
    const newPassword = event.target.value;
    setPassword(newPassword);
    setIsPasswordValid(newPassword.length >= 8 && /[a-z]/.test(newPassword) && /[A-Z]/.test(newPassword));
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    user = {
      name : name,
      email : email,
      password : password,
      phone : phone,
      address : address,
      postalcode : postalcode
    }
    console.log(user);
    await signup(user)
      .then((response) => {
        console.log(response.data);;
        setShowOtpModal(true);
      })
      .catch((error) => {
        console.log(error);
        if (error.response && error.response.status != 400) {
          setErrorMessage('SignUp failed. Please try again.');
        }
      })
  };

  const handleOtpSubmit = (event) => {
    // TODO: Handle OTP submission logic
    event.preventDefault();
    otp_verification = {
      username : email,
      otp : +otp
    }
    console.log(otp_verification);
    verify_email(otp_verification)
      .then((response) => {
        console.log(response.data);;
        navigate("/Login");
      })
      .catch((error) => {
        console.log(error);
      });
    setShowOtpModal(false);
  }
  
  function Login() {
    navigate('/Login');
  };

  return (

    <div className="bg-white w-full h-screen pt-4">     
      <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 pl-4 font-extrabold">Student Marketplace </h2>
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
      
      <div className="bg-white px-popup2 pb-24">
        <h2 className="text-2xl font-semibold text-gray-600">SignUp</h2>
        <p className="font-medium text-sm text-gray-400 mt-2">
        Use your Dalhousie credentials to sign up
        </p>
        
        <div className="mt-6">
        <div>
          <label className="text-lg font-medium">Name</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="Tiger"
            id="name"
            value={name} 
            onChange={e => setName(e.target.value)}
          />
        </div>
        <div className="mt-2">
          <label className="text-lg font-medium">Email</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="tiger@dal.ca"
            id="email"
            type={"email"}
            value={email} 
            onChange={handleEmailChange} required 
            />
          {!isEmailValid && <p className="text-sm pl-2 text-red-500 italic">Must be a dal.ca email</p>}
        </div>
        <div className="mt-2">
          <label className="text-lg font-medium">Password</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="tiger@123"
            id="password"
            type={"password"}
            value={password} 
            onChange={handlePasswordChange} required />
        {!isPasswordValid && (
          <p className="text-sm pl-2 text-red-500 italic">
            Must have at least 8 characters and contain at least one uppercase and one lowercase letter
          </p>
        )}
        </div>
        <div className="mt-2">
          <label className="text-lg font-medium">Phone Number</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="+1 234 567 8910"
            id="phone"
            type={"tel"}
            value={phone} 
            onChange={e => setPhone(e.target.value)}
          />
        </div>
        <div className="mt-2">
          <label className="text-lg font-medium">Address</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="6299 South St, Halifax, NS"
            id="address"
            type={"text"}
            value={address} 
            onChange={e => setAddress(e.target.value)}
          />
        </div>
        <div className="mt-2">
          <label className="text-lg font-medium">Postal Code</label>
          <input
            className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent italic"
            placeholder="B3H 4R2"
            id="postalcode"
            type={"text"}
            value={postalcode} 
            onChange={e => setPostalcode(e.target.value)}
          />
        </div>
        <div className="mt-4 text-red-500 italic">{errorMessage}</div>
        <div className="mt-8 flex flex-col gap-y-4">
          <button type="submit" onClick={handleSubmit} className="active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-bold">
            Sign Up
          </button>
        </div>
        <div className=" mt-4 flex justify-center items-center">
          <button type="button" onClick={Login} className="italic font-medium text-base hover:underline decoration-[2px] decoration-[#FFD400] ml-2">
            Already have an account? Login
          </button>
        </div>
      </div>

      <Modal show={showOtpModal} onHide={() => setShowOtpModal(false)}>
        <div class="fixed top-1/2 left-1/2 w-screen h-screen items-center justify-center transform -translate-x-1/2 -translate-y-1/2 bg-gray-100 rounded-xl shadow-md">
          <div class="container mx-auto">
              <div class="max-w-sm mx-auto md:max-w-lg">
                  <div class="w-full">
                      <div class="bg-white h-64 py-3 rounded-3xl text-center">
                            <h1 class="text-2xl font-bold">OTP Verification</h1>
                            <div class="flex flex-col mt-4">
                                <span>Enter the OTP you received at</span>
                                <span class="font-bold">{email}</span>
                            </div>
                            
                            <div id="otp" class="flex flex-row justify-center text-center px-2 mt-5">
                             <input class="m-2 border h-10 w-60 text-center form-control rounded" 
                             type="text" 
                             id="first" 
                             maxLength="6" 
                             value={otp} 
                             onChange={(e) => setOtp(e.target.value)}
                             /> 
                            </div>
                            
                            <div className="mt-8 flex flex-col gap-y-4">
                                <button size="lg" type="submit" onClick={handleOtpSubmit} className="active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#FFD400] text-black text-text-lg font-bold">
                                <span class="font-bold">
                                  Submit
                                  </span><i class='bx bx-caret-right ml-1'></i>
                                </button>
                            </div>
                      </div>
                  </div>
              </div>
          </div>
        </div>
      </Modal>
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
