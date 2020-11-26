const API_KEY = ''; // Put your API KEY here

CKEDITOR.config.embed_provider = `http://iframely.com/api/oembed?url={url}&callback={callback}&api_key={ ${API_KEY} }`;

CKEDITOR.replace('ckeditor', {
  extraPlugins: 'embed,autoembed,magicline' });


// VERSION_NUMBER = 4.5.11
// DISTRIBUTION = standard-all

// list of editor plugins
// https://ckeditor.com/presets-all
// or if it isn't available, go to
// https://cdn.ckeditor.com/{VERSION_NUMBER}/{DISTRIBUTION}/plugins/