import * as React from "react";
import logo from '../../assets/logo.png';
import { Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { readImages } from "../../services/api-service";
import { getSeller } from "../../services/api-service";
import Modal from "react-bootstrap/Modal";

export default function Buy() {

  const location = useLocation();
  const { prodTitle, prodDescription, prodPrice, prodId, prodUserId, prodCategory } = location.state;
  const [imageDataUrl0, setImageDataUrl0] = useState('');
  const [imageDataUrl1, setImageDataUrl1] = useState('');
  const [imageDataUrl2, setImageDataUrl2] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    readImages(prodId)
    .then(response => {
    // Convert the encrypted image string to an image object
    const encryptedImageString0 = response.data.pi_primImage; // Replace with the actual property name
    const imageMimeType0 = 'image/png'; // Replace with the actual MIME type
    const imageDataUrl0 = `data:${imageMimeType0};base64,${encryptedImageString0}`; 
    setImageDataUrl0(imageDataUrl0);

    const encryptedImageString1 = response.data.pi_secImage; // Replace with the actual property name
    const imageMimeType1 = 'image/png'; // Replace with the actual MIME type
    const imageDataUrl1 = `data:${imageMimeType1};base64,${encryptedImageString1}`; 
    setImageDataUrl1(imageDataUrl1);

    const encryptedImageString2 = response.data.pi_terImage; // Replace with the actual property name
    const imageMimeType2 = 'image/png'; // Replace with the actual MIME type
    const imageDataUrl2 = `data:${imageMimeType2};base64,${encryptedImageString2}`;
    setImageDataUrl2(imageDataUrl2); 
    console.log(prodTitle);
    console.log(prodDescription);
    console.log(prodUserId);
    })
    .catch(error => {
      console.error(error);
    });
  }, []);

  const [sellerInfo, setSellerInfo] = useState(null);
  // const prodUserId = "some user id"; // replace with the actual user id

  const handleContactSellerClick = async () => {
    try {
      const response = await getSeller(prodUserId);
      setSellerInfo(response.data);
      setShowModal(true);
      // console.log("Seller Info: ", sellerInfo);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    console.log("Seller Info: ", sellerInfo);
  }, [sellerInfo]);

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="bg-white w-full h-screen pt-4">
    
    <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 pl-4 font-extrabold">Student Marketplace </h2>
      <hr/>

      <div className="pl-5">
        <p className="font-bold text-2xl pb-1 text-black mt-2">
          Product Details
        </p>
        <p className="font-medium text-base text-gray-500">
          {prodCategory}
        </p>
      </div>

  <div>

    <div class="mx-auto mt-6 max-w-2xl sm:px-6 lg:grid lg:max-w-7xl lg:grid-cols-3 lg:gap-x-8 lg:px-8">
      <div class="aspect-w-3 aspect-h-4 hidden overflow-hidden rounded-lg lg:block">
        <img src={imageDataUrl0} alt="Two each of gray, white, and black shirts laying flat." class="h-full w-full object-cover object-center"/>
      </div>
      <div class="aspect-w-4 aspect-h-5 sm:overflow-hidden sm:rounded-lg lg:aspect-w-3 lg:aspect-h-4">
        <img src={imageDataUrl1} alt="Model wearing plain white basic tee." class="h-full w-full object-cover object-center"/>
      </div>
      <div class="aspect-w-4 aspect-h-5 sm:overflow-hidden sm:rounded-lg lg:aspect-w-3 lg:aspect-h-4">
        <img src={imageDataUrl2} alt="Model wearing plain white basic tee." class="h-full w-full object-cover object-center"/>
      </div>
    </div>

 
    <div class="mx-auto max-w-2xl px-4 pt-10 pb-16 sm:px-6 lg:grid lg:max-w-7xl lg:grid-cols-3 lg:grid-rows-[auto,auto,1fr] lg:gap-x-8 lg:px-8 lg:pt-16 lg:pb-24">
    <Modal show={showModal} onHide={handleCloseModal}>
            <div class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-100 rounded-xl shadow-md w-96">
              <div class="container mx-auto">
                <div class="max-w-sm mx-auto md:max-w-lg">
                  <div class="w-full">
                    <div class="bg-white h-64 py-3 rounded-3xl text-center">
                      <h1 class="text-2xl font-bold">Seller Details</h1>
                      <div class="flex flex-col mt-4">
                        {sellerInfo && (
                          <>
                            <span>{sellerInfo.u_name}</span>
                            <span class="font-bold">{sellerInfo.u_email}</span>
                            <span class="font-bold">{sellerInfo.u_phone}</span>
                          </>
                        )}
                      </div>
                      <div className="mt-8 flex flex-col gap-y-4">
                        <button
                          variant="secondary"
                          onClick={handleCloseModal}
                          className="active:scale-[.98] active:duration-75 hover:scale-[1.01] ease-in-out transition-all py-3 rounded-xl bg-[#ffd711] text-black text-text-lg font-bold"
                        >
                          Close
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Modal> 
      <div class="lg:col-span-2 lg:border-r lg:border-gray-200 lg:pr-8 pt-4">
        <h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">{prodTitle}</h1>
      </div>

    
      <div class="mt-4 lg:row-span-3 lg:mt-0">

        <p class="text-3xl text-center tracking-tight text-gray-900 pt-4">${prodPrice}</p>

        <form class="mt-10" onSubmit={(e) => e.preventDefault()}>
          <button 
          type="submit" 
          onClick={handleContactSellerClick}
          class="mt-10 flex w-full items-center justify-center rounded-md border border-transparent bg-yellow-400 py-3 px-8 text-base font-medium text-black hover:bg-yellow-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
            Contact Seller to Buy
          </button>
          
        </form>
      </div>

      <div class="py-10 lg:col-span-2 lg:col-start-1 lg:border-r lg:border-gray-200 lg:pt-6 lg:pb-4 lg:pr-8">
      
        <div>
          <div class="space-y-6">
            <p class="text-base text-justify text-gray-900">{prodDescription}</p>
          </div>
        </div>

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
