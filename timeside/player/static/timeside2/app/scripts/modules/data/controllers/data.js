define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      /*A.vent.on(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/

      A._v.onCfg('data.items.get','',this.onGetItems,this);
      A._v.onCfg('data.items.getOne','',this.onGetOneItem,this);
    },

    onDestroy : function() {
      /*A.vent.off(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/


      A._v.offCfg('data.items.get','',this.onGetItems,this);
      A._v.offCfg('data.items.getOne','',this.onGetOneItem,this);
     
    },

    /////////////////////////////////////////////////////////////////////
    // Get Items

    onGetItems:function() {
       A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.get),null,null,
        function(result) {
          //alert('oui');
          A._i.setOnCfg('allItems',result);
          return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.data.items.get));
        }, function(error) {
          alert("Non1");
      });
    },

     /////////////////////////////////////////////////////////////////////
    // Get One Item & nivigate to view
    onGetOneItem:function(id,viewid) {

      console.error("Temp : get one item does not work direct from list");


      var item = _.find(A._i.getOnCfg('allItems'),function(it) {return it.get('uuid')===id});
      if (item) {
        A._i.setOnCfg('currentItem',item);

        //new : get all annotations on item
        return this.getAllAnotations(item,function(result) {
          item.set('annotationTracksObjects',result);
          return A._v.trigCfg('navigate.page','',viewid);
        });

      }
      return;

      A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.getOne),{id : id},null,
        function(result) {
          A._i.setOnCfg('currentItem',result);
          var _viewid = viewid || 'item_view';
          return A._v.trigCfg('navigate.page','',_viewid);
        }, function(error) {
          alert("Non1");
      });
    },


    //get all annotations
    getAllAnotations:function(item,callback) {
        var indexCurrentAnnotation = 0;
        var result = [];

        if ( (!item.get('annotation_tracks')) || item.get('annotation_tracks').length==0 )
          return callback();

        var getNewAnnotation = function() {
          if (indexCurrentAnnotation >= item.get('annotation_tracks').length)
            return callback(result);

          var urlAnnotation = item.get('annotation_tracks')[indexCurrentAnnotation];
          $.get(urlAnnotation,function(res) {
              result.push(res);
              indexCurrentAnnotation++;
              return getNewAnnotation();
          });
        };

        return getNewAnnotation();  

    }   


  

   

  });
});
