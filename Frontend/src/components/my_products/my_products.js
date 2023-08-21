import * as React from "react";
import logo from '../../assets/logo.png';
import './my_products.css';
import { useState, useEffect } from 'react';
// import { getting_allProducts } from "../../services/api-service";
import { Link } from 'react-router-dom';
import { getting_myProducts } from "../../services/api-service";
import { delete_post } from "../../services/api-service";
import { getUser } from "../../services/api-service";

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function My_Product() {

  const [products, setProducts] = useState([]);

  useEffect(() => {
    getting_myProducts()
      .then(response => {
        setProducts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  // Declare empty arrays to store values
  const address = [];
  const category = [];
  const description = [];
  const id = [];
  const price = [];
  const prodStatus = [];
  const title = [];
  const user_id = [];
  const prodTitle = [];
  const prodImages = [];
  const prodPrice = [];
  const prodDescription = [];
  const prodId = [];
  const prodUserId = [];

  // Populate the arrays with the data stored in the state variable
  products.forEach(product => {
    address.push(product.address);
    category.push(product.category);
    description.push(product.description);
    id.push(product.id);
    price.push(product.price);
    prodStatus.push(product.status);
    title.push(product.title);
    user_id.push(product.user_id);
    prodTitle.push(product.title); 
    prodPrice.push(product.price); 
    prodDescription.push(product.description); 
    prodId.push(product.id); 
    prodUserId.push(product.user_id);

    // Convert the encrypted image string to an image object
    const encryptedImageString = product.titImage; // Replace with the actual property name
    const imageMimeType = 'image/png'; // Replace with the actual MIME type
    const imageDataUrl = `data:${imageMimeType};base64,${encryptedImageString}`; 
    const image = new Image();
    image.src = imageDataUrl;
    prodImages.push(imageDataUrl); 
    console.log(prodStatus)
  });

  const handleSubmit = async (event, prodId) => {
    event.preventDefault();
    // const form = event.target;
  
    await delete_post(prodId)
    .then((response) => {
      console.log(response.data);
      // window.location.reload();
      // navigate('/MyProducts');
      getting_myProducts()
      .then(response => {
        setProducts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
    })
    .catch((error) => {
      console.log(error);
    });
  }

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

      <div className="buying_nav">
        <div class="relative inline-block text-left">

        <Link to="/WelcomePage"><b>&nbsp;&nbsp;Home&nbsp;&nbsp;</b></Link>

        </div>
      </div>
      

      <div className="pl-5">
         <p className="font-bold text-2xl pb-1 text-black mt-2">
         <h2 className="text-2xl font-semibold">Hi {user.u_name}!</h2>
         </p>
         <p className="font-medium text-base text-gray-500">
           Your All Products
         </p>
       </div>

      <section class="bg-white">

        <div class="mx-auto max-w-2xl py-16 px-4 sm:py-12 sm:px-6 lg:max-w-7xl lg:px-8">

          <div class="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
            {prodImages.map((image, index) => (
              <div class="p-2">
                <div class="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-w-7 xl:aspect-h-8">
                  <img key={index} src={image} alt={`Product ${index}`} class="h-full w-full object-cover object-center group-hover:opacity-75"/>
                  {/* <img src={`data:image/jpeg;base64,${data}`} /> */}
                </div>
                <h3 class="mt-4 text-sm text-gray-700">{prodTitle[index]}</h3>
                <p class="mt-1 text-lg font-medium text-gray-900">${prodPrice[index]}</p>
                <form class="mt-1">
                  <button
                  className={classNames(
                    'flex justify-center rounded-md py-2 px-3 text-base',
                    prodStatus[index] === "Deleted" ? 'bg-gray-300' : 'bg-yellow-400 hover:bg-yellow-500 text-black'
                  )}
                  onClick={(event) => handleSubmit(event, prodId[index])}>
                    {prodStatus[index] === 'Deleted' ? 'Sold' : 'Mark as Sold'}
                  </button>
                </form>
              </div>
              ))}
          </div>
        </div>

      </section>
      
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

