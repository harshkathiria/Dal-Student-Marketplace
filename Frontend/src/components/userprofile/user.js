import React from "react";
import { useState } from "react";
import logo from '../../assets/logo.png';
import { Link } from 'react-router-dom';
import './user.css';
import { getUser } from "../../services/api-service";
import { useEffect } from 'react';

export default function UserDetails() {

  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getUser();
        setUser(response.data);
      } catch (error) {
        console.log(error);
      }
    };
    fetchData();
  }, []);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (

    <div className="bg-white w-full h-screen pt-4">

      <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 pl-4 font-extrabold">Student Marketplace </h2>
      <hr/>

      <div className="user_nav">

        <div class="relative inline-block">

        <Link to="/MyProducts"><b>&nbsp;&nbsp;Your Items&nbsp;&nbsp;</b></Link>&nbsp;
        <Link to="/WelcomePage"><b>&nbsp;&nbsp;Home&nbsp;&nbsp;</b></Link>

        </div>
      </div>

      <div className="pl-5">
        <p className="font-bold text-2xl pb-1 text-black mt-2">
         <h2 className="text-2xl font-semibold">Welcome {user.u_name}!</h2> 
        </p>
      </div>
      
      <div className="bg-white px-popup pb-8">
        <h2 className="text-2xl font-semibold text-gray-500">Profile</h2>
        
        <div className=" mt-6">
          <div className="mb-4">
            <label className="text-lg font-medium">Name</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="text"
              value={user.u_name}
              disabled
            />
          </div>
          <div className="mb-4">
            <label className="text-lg font-medium">Email</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="text"
              value={user.u_email}
              disabled
            />
          </div>
          <div className="mb-4">
            <label className="text-lg font-medium">Password</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="password"
              value={user.u_password}
              disabled
            />
          </div>
          <div className="mb-4">
            <label className="text-lg font-medium">Phone Number</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="text"
              value={user.u_phone}
              disabled
            />
          </div>
          <div className="mb-4">
            <label className="text-lg font-medium">Address</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="text"
              value={user.u_address}
              disabled
            />
          </div>
          <div className="mb-4">
            <label className="text-lg font-medium">Postal Code</label>
            <input
              className="w-full border-2 border-gray-100 rounded-xl p-3 mt-1 bg-transparent"
              id="name"
              type="text"
              value={user.u_postalcode}
              disabled
            />
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
