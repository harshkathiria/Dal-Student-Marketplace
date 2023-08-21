import * as React from "react";
import logo from '../../assets/logo.png';
import './buying.css';
import { useState, useEffect } from 'react';
import { getting_allProducts } from "../../services/api-service";
import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import { Link } from 'react-router-dom';



import * as React from "react";
import logo from '../../assets/logo.png';
import './buying.css';
import { useState, useEffect } from 'react';
import { getting_allProducts } from "../../services/api-service";
import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/20/solid';
import { Link } from 'react-router-dom';




function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Buy() {

  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('Categories');
  console.log(selectedCategory);
  function handleSelectCategory(category) {
    setSelectedCategory(category);
    if (category === 'All') {
      setProducts(filteredProducts);
    } else {
      const filtered = filteredProducts.filter(product => product.category === category);
      setProducts(filtered);
    }
  }

  useEffect(() => {
    getting_allProducts()
      .then(response => {
        setProducts(response.data);
        setFilteredProducts(response.data);
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
  const status = [];
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
    status.push(product.status);
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
  });

  return (
      
    <div className="bg-white w-full h-screen pt-4">

      <img src={logo} className="App-logo" alt="logo" />
      <h2 className="text-2x text-center pb-4 pl-4 font-extrabold">Student Marketplace </h2>
      <hr/>

      <div className="buying_nav">

        <div class="relative inline-block text-left">

          <Menu as="div" className="relative inline-block text-left">
            <div className="pt-4 pr-4">
              <Menu.Button className="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              Categories
              <ChevronDownIcon className="-mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
              </Menu.Button>
            </div>

            <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Books')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Books
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Electronics')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Electronics
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Furniture')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Furniture
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Musical Instruments')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Musical Instruments
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Sports Equipments')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Sports Equipments
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('Others')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        Others
                      </a>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        onClick={() => handleSelectCategory('All')}
                        className={classNames(
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                          'block px-4 py-2 text-sm'
                        )}
                      >
                        All
                      </a>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
      
      <div className="pl-5">
        <p className="font-bold text-2xl pb-1 text-black mt-2">
          Buy Stuff!
        </p>
        <p className="font-medium text-base text-gray-500">
          Products on Sale
        </p>
      </div>

      <section class="bg-white">
        <div class="mx-auto max-w-2xl py-16 px-4 sm:py-12 sm:px-6 lg:max-w-7xl lg:px-8">
          <div class="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8">
            {prodImages.map((image, index) => (
              <Link class="group p-2" to={'/Product_Details'}
                  state= {{
                  prodTitle: prodTitle[index],
                  prodDescription: prodDescription[index],
                  prodPrice: prodPrice[index],
                  prodId: prodId[index],
                  prodUserId: prodUserId[index],
                  prodCategory: category[index],
              }}>
                <div class="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-w-7 xl:aspect-h-8">
                  <img key={index} src={image} alt={`Product ${index}`} class="h-full w-full object-cover object-center group-hover:opacity-75"/>
                  {/* <img src={`data:image/jpeg;base64,${data}`} /> */}
                </div>
                <h3 class="mt-4 text-sm text-gray-700">{prodTitle[index]}</h3>
                <p class="mt-1 text-lg font-medium text-gray-900">${prodPrice[index]}</p>
              </Link>
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