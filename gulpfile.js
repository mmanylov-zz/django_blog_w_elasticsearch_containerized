'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var header = require('gulp-header');
var cleanCSS = require('gulp-clean-css');
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var pkg = require('./package.json');
var sourcemaps = require('gulp-sourcemaps');
var $ = require('gulp-load-plugins')();


// Compiles SCSS files from /scss into /css
gulp.task('sass', function () {
  const AUTOPREFIXER_BROWSERS = [
    'ie >= 10',
    'ie_mob >= 10',
    'ff >= 30',
    'chrome >= 34',
    'safari >= 7',
    'opera >= 23',
    'ios >= 7',
    'android >= 4.4',
    'bb >= 10'
  ];
  return gulp.src('static/scss/main.scss')
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe($.autoprefixer(AUTOPREFIXER_BROWSERS))
    .pipe($.size({
      title: 'styles'
    }))
    .pipe(gulp.dest('static/css'))
});

// Minify compiled CSS
gulp.task('minify-css', ['sass'], function () {
  return gulp.src('static/css/main.css')
    .pipe(cleanCSS({
      compatibility: 'ie8'
    }))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('static/css'))
});

// Minify custom JS
gulp.task('minify-js', function () {
  return gulp.src('static/js/main.js')
    .pipe(uglify())
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('static/js'))
});

// Copy vendor files from /node_modules into /vendor
// NOTE: requires `npm install` before running!
gulp.task('copy', function () {
  gulp.src([
      'node_modules/bootstrap/dist/**/*',
      '!**/npm.js',
      '!**/bootstrap-theme.*',
      '!**/*.map'
    ])
    .pipe(gulp.dest('static/vendor/bootstrap'))

  gulp.src(['node_modules/jquery/dist/jquery.js', 'node_modules/jquery/dist/jquery.min.js'])
    .pipe(gulp.dest('static/vendor/jquery'))

  gulp.src(['node_modules/magnific-popup/dist/*'])
    .pipe(gulp.dest('static/vendor/magnific-popup'))

  gulp.src(['node_modules/scrollreveal/dist/*.js'])
    .pipe(gulp.dest('static/vendor/scrollreveal'))

  gulp.src(['node_modules/popper.js/dist/umd/popper.js', 'node_modules/popper.js/dist/umd/popper.min.js'])
    .pipe(gulp.dest('static/vendor/popper'))

  gulp.src(['node_modules/jquery.easing/*.js'])
    .pipe(gulp.dest('static/vendor/jquery-easing'))

  gulp.src(['node_modules/aos/dist/*.js', 'node_modules/aos/dist/*.css'])
    .pipe(gulp.dest('static/vendor/aos'))

  gulp.src([
      'node_modules/font-awesome/**',
      '!node_modules/font-awesome/**/*.map',
      '!node_modules/font-awesome/.npmignore',
      '!node_modules/font-awesome/*.txt',
      '!node_modules/font-awesome/*.md',
      '!node_modules/font-awesome/*.json'
    ])
    .pipe(gulp.dest('static/vendor/font-awesome'))
})


// Optimize images
gulp.task('images', () =>
  gulp.src('static/img/**/*.+(png|jpg|JPG|jpeg|gif|svg)')
  .pipe($.cache($.imagemin([
    $.imagemin.jpegtran({
      progressive: true
    }),
    $.imagemin.optipng({
      optimizationLevel: 5
    }),
  ])))
  .pipe(gulp.dest('static/img/compressed'))
  .pipe($.size({
    title: 'images'
  }))
);


// Default task
gulp.task('default', ['sass', 'minify-css', 'minify-js', 'copy']);


gulp.task('dev', ['sass', 'minify-css', 'minify-js'], function () {
  gulp.watch('scss/*.scss', ['sass']);
  gulp.watch('css/*.css', ['minify-css']);
  gulp.watch('js/*.js', ['minify-js']);
});