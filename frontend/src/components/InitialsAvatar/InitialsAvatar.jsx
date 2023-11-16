import React from 'react';

function InitialsAvatar({ username, className}) {
  function getInitials(name) {
    let initials = name.match(/\b\w/g) || [];
    initials = ((initials.shift() || '') + (initials.pop() || '')).toUpperCase();
    return initials;
  }

  const initials = getInitials(username);

  return (
    <div className={`flex items-center justify-center ${className} bg-bgColor rounded-full`}>
      <p className={`text-center font-thin text-main`}>
        {initials}
      </p>
    </div>
  );
}

export default InitialsAvatar;
