import * as React from "react";

// import React, { useState, useEffect } from 'react';
import logo from '../../assets/logo.png';
import img1 from '../../assets/dal_1.jpg';
import img2 from '../../assets/dal_2.jpg';
import img3 from '../../assets/dal_3.jpg';
import './homepage.css';
import { Link } from 'react-router-dom';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

export default function HomePage() {
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
        fade: true,
        cssEase: 'linear'
      };
    return (

      
      <div>
      <div className="App">
        <div className="header">

          <div className='logo'>
            <img src={logo} className="App-logo" alt="logo" />
          </div>

          <div className='header_text'>
            Student Marketplace
          </div>
        </div>
        <hr/>
        <div className="navigation-box">

        <b class="text-xl font-semibold">Welcome Guest!</b>

          <nav>
            <ul>
              <li>
                <Link to="/Login"><b>&nbsp;&nbsp;Login/SignUp&nbsp;&nbsp;</b></Link>
              </li>
            </ul>
          </nav>
        </div>

        <div className="slider" >

          <Slider {...settings}>
            <div>
              <img src={img1} />
            </div>
            <div>
              <img src={img2} />
            </div>
            <div>
              <img src={img3}/>
            </div>
          </Slider>

        </div>
<br></br>
<hr/>
        <div className="footer">

        <div className='footer_text1'>
            <b>Dalhousie University</b><br></br>
            Halifax, Nova Scotia, Canada B3H 4R2
        </div>

        <div className='footer_text2'>
          <Link className="footer_links" to="">&nbsp;About&nbsp;</Link>
          <Link className="footer_links" to="">&nbsp;Contact Us&nbsp;</Link>         
        </div>

        </div>

      </div>
    </div>
  );
}