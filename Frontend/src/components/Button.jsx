import React from 'react'

const Button = ({data}) => {
  return (
    <div className='cursor-pointer h-[6vh] text-white font-semibold px-3 py-3 bg-[#6872ff] text-md hover:bg-[#7f87ff] rounded-md w-fit'>
        <button className='cursor-pointer'>{data}</button>
    </div>
  )
}

export default Button